"""
Service untuk tracking progress retrain secara real-time
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Path to progress file - handle both local and Railway environments
try:
    PROGRESS_FILE = (
        Path(__file__).resolve().parents[4]
        / "Model IndoBERT"
        / "data"
        / "retrain_progress.json"
    )
except (IndexError, ValueError):
    # Railway/Docker - use temp directory
    PROGRESS_FILE = Path("/tmp/retrain_progress.json")


class RetrainProgress:
    """Singleton class untuk tracking retrain progress"""

    _instance = None
    _state: Dict[str, Any] = {
        "is_running": False,
        "progress": 0,  # 0-100
        "stage": "idle",  # idle, preparing, training, evaluating, saving, uploading, completed
        "message": "No retrain in progress",
        "started_at": None,
        "estimated_completion": None,
        "current_epoch": 0,
        "total_epochs": 3,
        "error": None,
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_state()
        return cls._instance

    def _load_state(self):
        """Load state dari file jika ada"""
        try:
            if PROGRESS_FILE.exists():
                with open(PROGRESS_FILE, "r") as f:
                    saved_state = json.load(f)
                    # Jika retrain terakhir gagal/incomplete, reset
                    if (
                        saved_state.get("is_running")
                        and saved_state.get("stage") != "completed"
                    ):
                        # Check jika sudah lebih dari 24 jam
                        started = saved_state.get("started_at")
                        if started and (time.time() - started) > 86400:  # 24 hours
                            logger.warning("Found stale retrain progress, resetting...")
                            self._reset_state()
                        else:
                            self._state.update(saved_state)
                    else:
                        self._state.update(saved_state)
        except Exception as e:
            logger.warning(f"Could not load retrain progress state: {e}")

    def _save_state(self):
        """Save state ke file"""
        try:
            PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(PROGRESS_FILE, "w") as f:
                json.dump(self._state, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save retrain progress state: {e}")

    def _reset_state(self):
        """Reset state ke default"""
        self._state = {
            "is_running": False,
            "progress": 0,
            "stage": "idle",
            "message": "No retrain in progress",
            "started_at": None,
            "estimated_completion": None,
            "current_epoch": 0,
            "total_epochs": 3,
            "error": None,
        }
        self._save_state()

    def start(self, total_epochs: int = 3):
        """Mulai tracking retrain"""
        self._state["is_running"] = True
        self._state["progress"] = 0
        self._state["stage"] = "preparing"
        self._state["message"] = "Preparing retrain..."
        self._state["started_at"] = time.time()
        self._state["total_epochs"] = total_epochs
        self._state["current_epoch"] = 0
        self._state["error"] = None
        # Estimate: ~10 hours for CPU training with 3 epochs
        self._state["estimated_completion"] = time.time() + (10 * 3600)
        self._save_state()
        logger.info("Retrain progress tracking started")

    def update(
        self,
        progress: int = None,
        stage: str = None,
        message: str = None,
        current_epoch: int = None,
        error: str = None,
    ):
        """Update progress"""
        if progress is not None:
            self._state["progress"] = min(100, max(0, progress))
        if stage:
            self._state["stage"] = stage
        if message:
            self._state["message"] = message
        if current_epoch is not None:
            self._state["current_epoch"] = current_epoch
            # Update progress based on epoch
            if self._state["total_epochs"] > 0:
                # Training is 10-80%, each epoch contributes equally
                epoch_progress = (current_epoch / self._state["total_epochs"]) * 70
                self._state["progress"] = int(10 + epoch_progress)
        if error:
            self._state["error"] = error
            self._state["is_running"] = False
            self._state["stage"] = "failed"

        self._save_state()
        logger.debug(
            f"Retrain progress: {self._state['progress']}% - {self._state['message']}"
        )

    def complete(
        self, success: bool = True, message: str = "Retrain completed successfully"
    ):
        """Mark retrain as completed"""
        self._state["is_running"] = False
        self._state["progress"] = 100
        self._state["stage"] = "completed" if success else "failed"
        self._state["message"] = message
        if not success and not self._state.get("error"):
            self._state["error"] = message
        self._save_state()
        logger.info(f"Retrain progress tracking completed: {message}")

    def get_state(self) -> Dict[str, Any]:
        """Get current state"""
        return self._state.copy()

    def reset(self):
        """Reset progress (for manual cleanup)"""
        self._reset_state()


# Singleton instance
progress_tracker = RetrainProgress()
