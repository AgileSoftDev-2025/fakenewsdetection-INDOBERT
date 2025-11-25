from __future__ import annotations

from dotenv import load_dotenv
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
load_dotenv()

import sys
from pathlib import Path
from typing import List, Optional

from fastapi.routing import APIRoute

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import logging
import httpx
from .api import related as related_router

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # ← TAMBAHKAN INI

# Ensure repo root on sys.path
HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[3]
MODEL_DIR = REPO_ROOT / "Model IndoBERT"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(MODEL_DIR) not in sys.path:
    sys.path.insert(0, str(MODEL_DIR))

app = FastAPI(title="FakeNews Detection API", version="0.1.0")

# ✅ CORS - Allow localhost, ngrok, dan production domain
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    # Tambahkan ngrok URL kalau pakai ngrok (tapi ini gak ideal)
    # "https://your-ngrok-url.ngrok.io",
]

# Kalau ada env var FRONTEND_URL, tambahkan
if os.getenv("FRONTEND_URL"):
    ALLOWED_ORIGINS.append(os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from .api import predict as predict_router
from .api import feedback as feedback_router
from .api import admin as admin_router
from .api import results as results_router

app.include_router(predict_router.router, prefix="")
app.include_router(feedback_router.router, prefix="")
app.include_router(admin_router.router, prefix="")
app.include_router(results_router.router, prefix="")
<<<<<<< Updated upstream
app.include_router(related_router.router, prefix="")
=======
>>>>>>> Stashed changes


@app.get("/health")
async def health():
    logger.info("Health check endpoint hit")  # ← TAMBAHKAN LOG
    return {"status": "ok"}


@app.on_event("startup")
def ensure_model_available():
    """If model files aren't present locally, attempt to download from Hugging Face hub."""
    try:
        from huggingface_hub import snapshot_download
    except Exception:
        logger.debug("huggingface_hub not installed; skipping HF model download")
        return

    hf_repo = os.environ.get("HF_MODEL_REPO")
    if not hf_repo:
        logger.debug("HF_MODEL_REPO not set; skipping HF model download")
        return

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
    except Exception as exc:
        logger.exception("Failed to download model snapshot from Hugging Face: %s", exc)
