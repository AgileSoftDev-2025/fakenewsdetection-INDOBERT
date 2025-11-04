r"""Upload local model folder to Hugging Face Hub.

Usage (PowerShell):
$env:HF_TOKEN = "<your-token>"
python .\scripts\upload_model_to_hf.py --local-dir "..\..\Model IndoBERT\models\indobert" --repo-id "AgileSoftDev-2025/indobert-model" --private

This script uses huggingface_hub.upload_folder which is convenient for one-shot uploads.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local-dir", required=True, help="Local model folder to upload"
    )
    parser.add_argument(
        "--repo-id", required=True, help="Hugging Face repo id, e.g. user/model-name"
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Mark repo private after upload (requires permissions)",
    )
    parser.add_argument(
        "--commit-msg", default="Upload model artifacts", help="Commit message"
    )
    args = parser.parse_args()

    try:
        from huggingface_hub import HfApi, upload_folder
    except Exception:
        print(
            "Please install huggingface_hub in your environment: pip install huggingface-hub"
        )
        raise

    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError(
            "HF_TOKEN environment variable not set. Create a token at https://huggingface.co/settings/tokens and export it before running this script."
        )

    local_dir = Path(args.local_dir).expanduser().resolve()
    if not local_dir.exists():
        raise RuntimeError(f"Local directory does not exist: {local_dir}")

    api = HfApi()
    # create repo if not exists
    try:
        api.create_repo(repo_id=args.repo_id, private=args.private, token=token)
        print(f"Created repo {args.repo_id}")
    except Exception:
        print(
            f"Repo {args.repo_id} may already exist or creation failed; attempting upload"
        )

    print(f"Uploading folder {local_dir} to {args.repo_id} ...")
    upload_folder(
        folder_path=str(local_dir),
        path_in_repo=".",
        repo_id=args.repo_id,
        token=token,
        commit_message=args.commit_msg,
    )
    print("Upload complete. Visit https://huggingface.co/" + args.repo_id)


if __name__ == "__main__":
    main()
