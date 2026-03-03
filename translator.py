import logging

logger = logging.getLogger(__name__)

_MODEL_NAME = "Helsinki-NLP/opus-mt-ru-en"
_REVISION = "main" 
_tokenizer = None
_model = None


def preload_translation_model() -> None:
    try:
        _get_model()
        logger.info("Translation model preloaded")
    except Exception as e:
        logger.warning("Translation model preload failed: %s", e)


def _get_model():
    global _tokenizer, _model
    if _model is None:
        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
            import torch
            _tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME, revision=_REVISION)
            _model = AutoModelForSeq2SeqLM.from_pretrained(_MODEL_NAME, revision=_REVISION)
            _model.eval()
            device = "cuda" if __import__("torch").cuda.is_available() else "cpu"
            _model = _model.to(device)
            logger.info("Loaded Helsinki-NLP/opus-mt-ru-en translation model (device=%s)", device)
        except Exception as e:
            logger.warning("Translation model not available: %s", e)
            raise
    return _tokenizer, _model


def translate_ru_to_en(text: str) -> str:

    if not text or not str(text).strip():
        return ""

    text = str(text).strip()
    try:
        tokenizer, model = _get_model()
        import torch
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(model.device)
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=512)
        decoded = tokenizer.decode(out[0], skip_special_tokens=True)
        return decoded.strip() or text
    except Exception as e:
        logger.warning("Translation failed: %s", e)
        return text


def is_likely_russian(text: str) -> bool:
    if not text:
        return False
    return bool(__import__("re").search(r"[\u0400-\u04FF]", str(text)))


def prepare_text_for_mbti(text: str) -> str:

    if not text or not str(text).strip():
        return ""
    return translate_ru_to_en(text) if is_likely_russian(text) else str(text).strip()
