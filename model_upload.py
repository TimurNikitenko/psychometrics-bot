import argparse
import os
import sys
import tempfile

# Add project root for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from huggingface_hub import HfApi, create_repo
from transformers import AutoTokenizer, AutoModelForSequenceClassification


DEFAULT_TARGET_REPO = "TimurNikitenko/mbti-classifier-ru"
REPO_TYPE = "model"


def main():
    parser = argparse.ArgumentParser(
        description="Push local classifier to Hugging Face Hub"
    )
    parser.add_argument(
        "model_dir",
        nargs="?",
        default=None,
        help="Local path: directory containing model (and tokenizer), or directory with model/ and tokenizer/ subdirs",
    )
    parser.add_argument(
        "--model-dir",
        dest="model_dir_flag",
        default=None,
        help="Same as positional model_dir (optional form)",
    )
    parser.add_argument(
        "--target-repo",
        default=DEFAULT_TARGET_REPO,
        help=f"Target HF repo. Default: {DEFAULT_TARGET_REPO}",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("HF_TOKEN"),
        help="Hugging Face token (or set HF_TOKEN)",
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Create target repo as private if it does not exist",
    )
    parser.add_argument(
        "--subfolder",
        default="mbti-classifier",
        help="Path inside the repo (default: mbti-classifier). Use so this model does not overwrite event-classifier or others.",
    )
    args = parser.parse_args()

    model_dir = args.model_dir or args.model_dir_flag
    if not model_dir or not os.path.isdir(model_dir):
        parser.error(
            "A local model directory is required (e.g. ./classificator/saved_model)"
        )

    if not args.token:
        print("Error: HF_TOKEN is required. Set env HF_TOKEN or use --token.")
        sys.exit(1)

    model_dir = os.path.abspath(model_dir)
    target_repo = args.target_repo.strip()
    api = HfApi(token=args.token)

    # Resolve model and tokenizer paths (support both single dir and model/ + tokenizer/ subdirs)
    model_path = os.path.join(model_dir, "model")
    tokenizer_path = os.path.join(model_dir, "tokenizer")
    if os.path.isdir(model_path) and os.path.isdir(tokenizer_path):
        # Merge into one folder for HF (single root with both)
        with tempfile.TemporaryDirectory(prefix="classifier_upload_") as tmpdir:
            print(f"Loading from {model_dir} and merging into temp folder")
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
            model = AutoModelForSequenceClassification.from_pretrained(model_path)
            model.save_pretrained(tmpdir)
            tokenizer.save_pretrained(tmpdir)
            _ensure_repo_and_upload(api, tmpdir, target_repo, args.token, args.private, args.subfolder)
    else:
        # Single directory with both model and tokenizer files
        if not os.path.isfile(os.path.join(model_dir, "config.json")):
            print(
                "Error: model_dir must contain config.json, or model/ and tokenizer/ subdirs."
            )
            sys.exit(1)
        print(f"Uploading from {model_dir}")
        _ensure_repo_and_upload(api, model_dir, target_repo, args.token, args.private, args.subfolder)

    path_in_repo = f" ({args.subfolder}/)" if args.subfolder else " (repo root)"
    print(f"Done. Model available at: https://huggingface.co/{target_repo}{path_in_repo}")


def _ensure_repo_and_upload(
    api: HfApi,
    folder_path: str,
    target_repo: str,
    token: str,
    private: bool,
    path_in_repo: str | None = None,
):
    try:
        create_repo(
            repo_id=target_repo,
            repo_type=REPO_TYPE,
            private=private,
            token=token,
            exist_ok=True,
        )
    except Exception as e:
        print(f"Note: create_repo: {e}")

    # path_in_repo: upload into this subfolder so multiple models (event-classifier, mbti-classifier) don't overwrite each other
    msg = f"Uploading to https://huggingface.co/{target_repo}"
    if path_in_repo:
        msg += f" (path: {path_in_repo}/)"
    msg += " — only this path is updated; rest of repo unchanged"
    print(msg)
    upload_kw = dict(
        folder_path=folder_path,
        repo_id=target_repo,
        repo_type=REPO_TYPE,
        token=token,
        commit_message=f"Upload classifier to {path_in_repo or 'root'}; existing other files unchanged",
    )
    if path_in_repo:
        upload_kw["path_in_repo"] = path_in_repo
    api.upload_folder(**upload_kw)


if __name__ == "__main__":
    main()
