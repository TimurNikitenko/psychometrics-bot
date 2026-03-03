import logging
import os
import re
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm
try:
    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        get_linear_schedule_with_warmup,
    )
except ImportError as e1:
    try:
        from transformers import AutoTokenizer, get_linear_schedule_with_warmup
        from transformers.models.auto.modeling_auto import AutoModelForSequenceClassification
    except ImportError:
        raise ImportError(
            "Need transformers with AutoModelForSequenceClassification. "
            "Try: pip install -U 'transformers>=4.36.0'"
        ) from e1

logger = logging.getLogger(__name__)

# MBTI: 4 dichotomies, multi-label (one binary per dimension)
MBTI_TRAITS = ["I/E", "N/S", "T/F", "P/J"]
TRAIT_LETTERS = [("I", "E"), ("N", "S"), ("T", "F"), ("P", "J")]


def type_to_labels(mbti_type: str) -> list[float]:
    """Convert 4-letter MBTI type to 4 binary labels (1 = first letter of pair)."""
    mbti_type = (mbti_type or "").strip().upper()
    if len(mbti_type) != 4:
        raise ValueError(f"Invalid MBTI type: {mbti_type!r}")
    return [
        1.0 if mbti_type[i] == TRAIT_LETTERS[i][0] else 0.0
        for i in range(4)
    ]


def labels_to_type(labels: list[float]) -> str:
    """Convert 4 binary labels or probabilities to 4-letter MBTI type."""
    return "".join(
        TRAIT_LETTERS[i][0] if (labels[i] >= 0.5) else TRAIT_LETTERS[i][1]
        for i in range(4)
    )


def _preprocess_text(text: str) -> str:
        if not isinstance(text, str) or len(text) == 0:
            return ""

        html_pattern = re.compile(r"<[^>]+>")
        url_pattern = re.compile(r"https?://[^\s]+")
        mail_pattern = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
        phone_pattern = re.compile(r"[\+]?[0-9\s\-\(\)]{10,}")
        multiple_spaces = re.compile(r"\s+")

        # убираем html теги
        text = html_pattern.sub("", text)

        # заменяем ссылки
        text = url_pattern.sub("", text)
        # заменяем почту
        text = mail_pattern.sub("", text)

        # заменяем телефоны
        text = phone_pattern.sub("", text)

        # приводим к lowercase
        text = text.lower()

        # заменяем множественные пробелы на один пробел
        text = multiple_spaces.sub(" ", text)

        # удаляем лишние знаки (но оставляем точки, запятые)
        text = re.sub(r"[^\w\s\.,!?]", " ", text)

        text = text.strip()
        return text


HF_SUBFOLDER_MBTI = "mbti-classifier"


def _is_hf_repo(path: str) -> bool:
    """True if path looks like a Hugging Face repo id (owner/repo), not a local path."""
    if not path or not path.strip():
        return False
    path = path.strip()
    if os.path.isdir(path) or Path(path).expanduser().resolve().is_dir():
        return False
    return "/" in path and not path.startswith(".")


class MBTIClassifier:
    """
    Multi-label classifier for MBTI (4 dichotomies).
    Expects English text; for Russian, translate first (e.g. translator.translate_ru_to_en).
    Load via from_pretrained(path): path can be HF repo (e.g. TimurNikitenko/mbti-classifier-ru),
    local directory, or None for default distilbert-base-uncased.
    """

    def __init__(
        self,
        model_name: str = "distilbert-base-uncased",
        max_length: int = 512,
        device: Optional[torch.device] = None,
    ):
        self.model_name = model_name
        self.max_length = max_length
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=4,
            problem_type="multi_label_classification",
        )
        self.model = self.model.to(self.device)
        logger.info(f"MBTI classifier loaded on {self.device}")

    @classmethod
    def from_pretrained(
        cls,
        path: Optional[str] = None,
        *,
        max_length: int = 512,
        device: Optional[torch.device] = None,
        hf_subfolder: str = HF_SUBFOLDER_MBTI,
    ):
        """
        Load classifier from Hugging Face repo, local directory, or use default distilbert.
        path: HF repo id (e.g. TimurNikitenko/mbti-classifier-ru), local dir path, or None.
        """
        if not path or not path.strip():
            return cls(max_length=max_length, device=device)
        path = path.strip()
        if _is_hf_repo(path):
            inst = cls.__new__(cls)
            inst.model_name = path
            inst.max_length = max_length
            inst.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
            inst.tokenizer = AutoTokenizer.from_pretrained(path, subfolder=hf_subfolder)
            inst.model = AutoModelForSequenceClassification.from_pretrained(
                path, subfolder=hf_subfolder
            )
            inst.model = inst.model.to(inst.device)
            logger.info("MBTI classifier loaded from HF %s (subfolder=%s) on %s", path, hf_subfolder, inst.device)
            return inst
        # Local directory
        path_obj = Path(path).expanduser().resolve()
        if not path_obj.is_dir():
            raise FileNotFoundError(f"Model path is not a directory: {path}")
        inst = cls(max_length=max_length, device=device)
        inst.load(str(path_obj))
        return inst

    def load_data(
        self,
        csv_path: str,
        text_column: str = "posts",
        type_column: str = "type",
    ) -> tuple[list[str], list[list[float]]]:
        """Load MBTI CSV with columns type_column and text_column. Returns (texts, list of 4 labels)."""
        path = Path(csv_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {csv_path}")

        df = pd.read_csv(path)
        if type_column not in df.columns or text_column not in df.columns:
            raise ValueError(
                f"CSV must have columns {type_column!r} and {text_column!r}; got {list(df.columns)}"
            )

        texts = []
        labels = []
        for _, row in df.iterrows():
            t = (row[text_column] or "").strip()
            if not t or len(t) < 20:
                continue
            try:
                lab = type_to_labels(str(row[type_column]).strip())
            except (ValueError, TypeError):
                continue
            texts.append(_preprocess_text(t))
            labels.append(lab)

        logger.info(f"Loaded {len(texts)} samples from {csv_path}")
        return texts, labels

    def train(
        self,
        csv_path: str,
        output_dir: str,
        num_epochs: int = 5,
        batch_size: int = 8,
        val_size: float = 0.2,
        lr: float = 2e-5,
        patience: int = 3,
        text_column: str = "posts",
        type_column: str = "type",
    ) -> dict:
        """Train on CSV and save best model to output_dir. Returns dict with macro_f1, exact_match_accuracy."""
        texts, labels = self.load_data(csv_path, text_column=text_column, type_column=type_column)
        if not texts:
            return {"error": "no valid samples"}

        labels_arr = np.array(labels)
        logger.info(f"Dataset size: {len(labels_arr)}")
        logger.info(f"Label balance (1s per trait): {[f'{labels_arr[:, j].mean():.2f}' for j in range(4)]}")

        types = [labels_to_type(list(l)) for l in labels]
        try:
            train_idx, val_idx = train_test_split(
                range(len(texts)), test_size=val_size, random_state=42, stratify=types
            )
        except ValueError:
            train_idx, val_idx = train_test_split(
                range(len(texts)), test_size=val_size, random_state=42
            )
        train_idx, val_idx = np.array(train_idx), np.array(val_idx)

        train_labels_np = labels_arr[train_idx]
        pos_weights = []
        for j in range(4):
            n_pos = max(1, int(train_labels_np[:, j].sum()))
            n_neg = max(1, len(train_labels_np) - n_pos)
            pos_weights.append(n_neg / n_pos)
        pos_weight_t = torch.tensor(pos_weights, dtype=torch.float32).to(self.device)
        criterion = torch.nn.BCEWithLogitsLoss(pos_weight=pos_weight_t)

        encodings = self.tokenizer(
            texts,
            truncation=True,
            max_length=self.max_length,
            padding=True,
            return_tensors="pt",
        )
        input_ids = encodings["input_ids"]
        attention_mask = encodings["attention_mask"]
        labels_t = torch.tensor(labels, dtype=torch.float32)

        train_ids = input_ids[train_idx]
        val_ids = input_ids[val_idx]
        train_mask = attention_mask[train_idx]
        val_mask = attention_mask[val_idx]
        train_labels = labels_t[train_idx]
        val_labels = labels_t[val_idx]

        train_ds = TensorDataset(
            train_ids.to(self.device),
            train_mask.to(self.device),
            train_labels.to(self.device),
        )
        val_ds = TensorDataset(
            val_ids.to(self.device),
            val_mask.to(self.device),
            val_labels.to(self.device),
        )
        train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=batch_size)

        optimizer = torch.optim.AdamW(self.model.parameters(), lr=lr, weight_decay=0.01)
        total_steps = len(train_loader) * num_epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=int(0.1 * total_steps),
            num_training_steps=total_steps,
        )

        best_f1 = 0.0
        best_exact = 0.0
        best_state = None
        no_improve = 0
        from sklearn.metrics import f1_score

        for epoch in range(num_epochs):
            self.model.train()
            train_loss_sum = 0.0
            for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}"):
                iids, mask, lab = batch
                optimizer.zero_grad()
                out = self.model(input_ids=iids, attention_mask=mask)
                loss = criterion(out.logits, lab)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                optimizer.step()
                scheduler.step()
                train_loss_sum += loss.item()

            avg_train_loss = train_loss_sum / len(train_loader)

            # Validation
            self.model.eval()
            all_preds = []
            all_labels = []
            with torch.no_grad():
                for iids, mask, lab in val_loader:
                    out = self.model(input_ids=iids, attention_mask=mask)
                    probs = torch.sigmoid(out.logits)
                    all_preds.append((probs > 0.5).long().cpu())
                    all_labels.append(lab.cpu())
            preds = torch.cat(all_preds, dim=0).numpy()
            labels_np = torch.cat(all_labels, dim=0).numpy()

            pred_counts = [int(preds[:, j].sum()) for j in range(4)]
            label_counts = [int(labels_np[:, j].sum()) for j in range(4)]
            logger.info(f"Epoch {epoch+1} — Train loss: {avg_train_loss:.4f}")
            logger.info(f"Epoch {epoch+1} — Val: pred 1s per trait (I/E, N/S, T/F, P/J): {pred_counts} (total val samples: {len(preds)})")
            logger.info(f"Epoch {epoch+1} — Val: true 1s per trait: {label_counts}")

            per_label_f1 = []
            for j in range(4):
                f1_j = f1_score(labels_np[:, j], preds[:, j], average="binary", zero_division=0)
                per_label_f1.append(f1_j)
            macro_f1 = float(np.mean(per_label_f1))
            exact = np.all(preds == labels_np, axis=1).mean()

            logger.info(f"Epoch {epoch+1} — Per-trait F1 (I/E, N/S, T/F, P/J): {[f'{x:.4f}' for x in per_label_f1]}")
            logger.info(f"Epoch {epoch+1} — macro_f1: {macro_f1:.4f}, exact_match: {exact:.4f}")
            if macro_f1 > best_f1:
                best_f1 = macro_f1
                best_exact = exact
                best_state = {k: v.cpu().clone() for k, v in self.model.state_dict().items()}
                no_improve = 0
                logger.info(f"New best model (macro_f1={macro_f1:.4f}).")
            else:
                no_improve += 1
                logger.info(f"No improvement ({no_improve}/{patience}).")
            if no_improve >= patience:
                logger.info(f"Early stopping at epoch {epoch + 1}")
                break

        if best_state:
            self.model.load_state_dict(best_state)
            logger.info("Loaded best model state from validation.")

        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        self.model.save_pretrained(out_path / "model")
        self.tokenizer.save_pretrained(out_path / "tokenizer")
        logger.info(f"Model saved to {output_dir}")

        return {"macro_f1": float(best_f1), "exact_match_accuracy": float(best_exact)}

    def predict(
        self,
        text: str,
        return_confidence: bool = True,
    ) -> tuple[str, Optional[dict]]:
        """
        Predict MBTI type from English text.
        Returns (mbti_type, confidence_dict or None).
        confidence_dict: per dichotomy probabilities, e.g. {"I/E": 0.8, "N/S": 0.3, ...}.
        """
        text = _preprocess_text(text or "")
        if not text or len(text) < 10:
            return "INFP", None  

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_length,
            padding=True,
        ).to(self.device)

        with torch.no_grad():
            out = self.model(**inputs)

        logits = out.logits[0].cpu()
        probs = torch.sigmoid(logits).numpy()
        pred_labels = [1 if p >= 0.5 else 0 for p in probs]
        mbti_type = "".join(
            TRAIT_LETTERS[i][pred_labels[i]] for i in range(4)
        )

        if return_confidence:
            conf = {}
            for i, name in enumerate(MBTI_TRAITS):
                conf[name] = float(probs[i])  
            return mbti_type, conf
        return mbti_type, None

    def predict_any_lang(
        self,
        text: str,
        return_confidence: bool = True,
    ) -> tuple[str, Optional[dict]]:
        """Predict MBTI from text in English or Russian (Russian is translated to English)."""
        if not text or not str(text).strip():
            return "INFP", None
        try:
            from translator import prepare_text_for_mbti
            text = prepare_text_for_mbti(str(text).strip())
        except Exception:
            text = str(text).strip()
        return self.predict(text, return_confidence=return_confidence)

    def load(self, path: str) -> None:
        """Load model and tokenizer from directory (must contain model/ and tokenizer/)."""
        path = Path(path)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            path / "model",
            num_labels=4,
            problem_type="multi_label_classification",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(path / "tokenizer")
        self.model = self.model.to(self.device)
        logger.info(f"MBTI model loaded from {path}")

    def save(self, path: str) -> None:
        """Save model and tokenizer to directory."""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        self.model.save_pretrained(path / "model")
        self.tokenizer.save_pretrained(path / "tokenizer")
        logger.info(f"MBTI model saved to {path}")

