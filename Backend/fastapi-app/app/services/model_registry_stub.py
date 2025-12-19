"""
Stub untuk src.services.model_registry - digunakan di Railway production

Di Railway, backend hanya melakukan API call ke HF Space, tidak menjalankan model lokal.
File ini menyediakan stub functions untuk menghindari ModuleNotFoundError.
"""

import logging
from typing import Optional, List, Dict, Any
from pathlib import Path
import json

logger = logging.getLogger(__name__)

# Use /tmp for registry in Railway
REGISTRY_FILE = Path("/tmp/model_registry.json")


def _read_registry() -> Dict[str, Any]:
    """Read model registry (stub for Railway)"""
    if REGISTRY_FILE.exists():
        try:
            with open(REGISTRY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read registry: {e}")
    
    # Return default registry structure
    return {
        "current_version": "v1.0.0",
        "versions": {
            "v1.0.0": {
                "version": "v1.0.0",
                "accuracy": 0.0,
                "f1_score": 0.0,
                "created_at": None,
                "source": "huggingface_space",
            }
        },
    }


def _write_registry(registry: Dict[str, Any]) -> bool:
    """Write model registry (stub for Railway)"""
    try:
        with open(REGISTRY_FILE, "w") as f:
            json.dump(registry, f, indent=2)
        logger.info(f"Registry saved to {REGISTRY_FILE}")
        return True
    except Exception as e:
        logger.error(f"Failed to write registry: {e}")
        return False


def get_current_version() -> str:
    """
    Return default model version untuk Railway production.
    
    Di local development, ini akan query dari Model IndoBERT/models/indobert_versions/.
    Di Railway, kita hanya return static version karena model di-host di HF Space.
    """
    registry = _read_registry()
    return registry.get("current_version", "v1.0.0")


def get_all_versions() -> List[str]:
    """Return list of all available model versions (stub for Railway)"""
    registry = _read_registry()
    return list(registry.get("versions", {}).keys())


def get_version_info(version: str) -> Optional[Dict[str, Any]]:
    """Get information about a specific model version (stub for Railway)"""
    registry = _read_registry()
    return registry.get("versions", {}).get(version)
