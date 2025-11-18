from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()  

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# Ensure repo root on sys.path so we can import Model IndoBERT/src
HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[3]
# Add the parent directory of 'src' to sys.path so 'import src' works
MODEL_DIR = REPO_ROOT / "Model IndoBERT"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(MODEL_DIR) not in sys.path:
    sys.path.insert(0, str(MODEL_DIR))

app = FastAPI(title="FakeNews Detection API", version="0.1.0")

# CORS for local Next.js dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://abcd1234.ngrok.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
# Routers
from .api import predict as predict_router  # noqa: E402
from .api import feedback as feedback_router  # noqa: E402
from .api import admin as admin_router  # noqa: E402
from .api import results as results_router

app.include_router(predict_router.router, prefix="")
app.include_router(feedback_router.router, prefix="")
app.include_router(admin_router.router, prefix="")
app.include_router(results_router.router, prefix="") 


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
def ensure_model_available():
    """If model files aren't present locally, attempt to download from Hugging Face hub.

    Environment variables:
    - HF_MODEL_REPO: repository id on HF hub (e.g. 'AgileSoftDev-2025/indobert-model')
    - HF_TOKEN: optional access token (if repo is private)

    This function will only run if huggingface_hub is installed and HF_MODEL_REPO is set.
    """
    try:
        from huggingface_hub import snapshot_download
    except Exception:  # pragma: no cover - optional dependency
        logger.debug("huggingface_hub not installed; skipping HF model download")
        return

    hf_repo = os.environ.get("HF_MODEL_REPO")
    if not hf_repo:
        logger.debug("HF_MODEL_REPO not set; skipping HF model download")
        return

    # Destination: keep the same structure as current Model IndoBERT/models/indobert
    dest_dir = REPO_ROOT / "Model IndoBERT" / "models" / "indobert"
    if dest_dir.exists() and any(dest_dir.iterdir()):
        logger.info("Model directory exists locally at %s, skipping download", dest_dir)
        return

    token = os.environ.get("HF_TOKEN")
    logger.info("Downloading model snapshot from %s to %s", hf_repo, dest_dir)
    try:
        snapshot_download(
            repo_id=hf_repo,
            cache_dir=str(REPO_ROOT / ".hf_cache"),
            local_dir=str(dest_dir),
            use_auth_token=token,
        )
        logger.info("Model snapshot downloaded to %s", dest_dir)
    except (
        Exception
    ) as exc:  # pragma: no cover - surface the error but do not crash the app
        logger.exception("Failed to download model snapshot from Hugging Face: %s", exc)
