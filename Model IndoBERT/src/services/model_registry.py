from __future__ import annotations

import json
import os
import shutil
import time
from typing import Any, Dict, Optional

from ..config import MODELS_DIR, SETTINGS


REGISTRY_DIR = os.path.join(MODELS_DIR, "indobert_versions")
REGISTRY_FILE = os.path.join(REGISTRY_DIR, "registry.json")


def _ensure_registry() -> None:
    os.makedirs(REGISTRY_DIR, exist_ok=True)
    if not os.path.exists(REGISTRY_FILE):
        data = {
            "current_version": "v1"
            if os.path.exists(SETTINGS.indobert_model_dir)
            else "v0",
            "history": [],
            "last_used_feedback_id": 0,
        }
        with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def _read_registry() -> Dict[str, Any]:
    _ensure_registry()
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_registry(data: Dict[str, Any]) -> None:
    os.makedirs(REGISTRY_DIR, exist_ok=True)
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_current_version() -> str:
    reg = _read_registry()
    return reg.get("current_version", "v0")


def get_last_used_feedback_id() -> int:
    reg = _read_registry()
    return int(reg.get("last_used_feedback_id", 0))


def set_last_used_feedback_id(row_id: int) -> None:
    reg = _read_registry()
    reg["last_used_feedback_id"] = int(row_id)
    _write_registry(reg)


def next_version() -> str:
    curr = get_current_version()
    try:
        n = int(curr.replace("v", ""))
    except Exception:
        n = 0
    return f"v{n + 1}"


def archive_and_set_current(
    new_version: str,
    metrics: Optional[Dict[str, Any]] = None,
    feedback_rows_used: int = 0,
) -> str:
    """
    Archive the model in SETTINGS.indobert_model_dir into a versioned folder and set current version in registry.
    Returns the path of archived model directory.
    """
    _ensure_registry()
    version_dir = os.path.join(REGISTRY_DIR, f"indobert_{new_version}")
    if os.path.exists(version_dir):
        # Should not overwrite existing version; append timestamp
        version_dir = version_dir + f"_{int(time.time())}"
    shutil.copytree(SETTINGS.indobert_model_dir, version_dir)

    reg = _read_registry()
    reg["current_version"] = new_version
    hist = reg.get("history", [])
    hist.append(
        {
            "version": new_version,
            "timestamp": int(time.time()),
            "metrics": metrics or {},
            "feedback_rows_used": int(feedback_rows_used),
        }
    )
    reg["history"] = hist
    _write_registry(reg)
    return version_dir


__all__ = [
    "get_current_version",
    "get_last_used_feedback_id",
    "set_last_used_feedback_id",
    "next_version",
    "archive_and_set_current",
]
