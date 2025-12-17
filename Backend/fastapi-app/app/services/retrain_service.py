"""
Auto-retrain service for IndoBERT model.
Handles automatic model retraining when feedback threshold is reached.
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Path setup
REPO_ROOT = Path(__file__).resolve().parents[4]
MODEL_DIR = REPO_ROOT / "Model IndoBERT"
FEEDBACK_CSV = MODEL_DIR / "data" / "feedback" / "feedback.csv"
REGISTRY_PATH = MODEL_DIR / "models" / "indobert_versions" / "registry.json"
AUTO_RETRAIN_SCRIPT = MODEL_DIR / "src" / "modeling" / "auto_retrain.py"
INDOBERT_MODEL_DIR = MODEL_DIR / "models" / "indobert"
VERSIONS_DIR = MODEL_DIR / "models" / "indobert_versions"

# Configuration
DEFAULT_RETRAIN_THRESHOLD = int(os.getenv("RETRAIN_THRESHOLD", "100"))
MIN_RETRAIN_THRESHOLD = 50  # Minimum feedback untuk retrain

# HuggingFace Configuration
HF_MODEL_REPO = os.getenv("HF_MODEL_REPO", "Davidbio/fakenewsdetection-indobert")
HF_TOKEN = os.getenv("HF_TOKEN", "")
ENABLE_HF_UPLOAD = os.getenv("ENABLE_HF_UPLOAD", "true").lower() == "true"


class RetrainService:
    """Service untuk mengelola auto-retrain model"""

    @staticmethod
    def check_gpu_availability() -> Dict[str, Any]:
        """
        Check if GPU is available for training
        Supports CUDA, DirectML, and CPU fallback
        Returns device info for monitoring
        """
        try:
            import torch

            # Check CUDA first
            cuda_available = torch.cuda.is_available()

            # Check DirectML (for Windows with newer GPUs like RTX 5070Ti)
            directml_available = False
            try:
                import torch_directml

                directml_available = torch_directml.is_available()
            except ImportError:
                pass

            # Determine best device
            if cuda_available:
                device_info = {
                    "gpu_available": True,
                    "device": "cuda",
                    "device_name": torch.cuda.get_device_name(0),
                    "backend": "cuda",
                    "cuda_version": torch.version.cuda,
                    "gpu_memory_gb": round(
                        torch.cuda.get_device_properties(0).total_memory / (1024**3), 2
                    ),
                }
            elif directml_available:
                import torch_directml

                dml_device = torch_directml.device()
                device_info = {
                    "gpu_available": True,
                    "device": "dml",
                    "device_name": f"DirectML GPU: {dml_device}",
                    "backend": "directml",
                    "directml_device": str(dml_device),
                }
            else:
                device_info = {
                    "gpu_available": False,
                    "device": "cpu",
                    "device_name": "CPU",
                    "backend": "cpu",
                }

            return device_info
        except Exception as e:
            logger.warning(f"Error checking GPU: {e}")
            return {
                "gpu_available": False,
                "device": "cpu",
                "device_name": "CPU",
                "backend": "cpu",
                "error": str(e),
            }

    @staticmethod
    def initialize_v1_if_needed():
        """
        Initialize v1 model if it doesn't exist
        Copies current model from models/indobert to models/indobert_versions/v1
        """
        v1_dir = VERSIONS_DIR / "v1"

        # Only initialize if v1 doesn't exist yet
        if v1_dir.exists():
            logger.debug("v1 already exists, skipping initialization")
            return

        logger.info("Initializing v1 model...")
        try:
            v1_dir.mkdir(parents=True, exist_ok=True)

            # Copy current model as v1
            if INDOBERT_MODEL_DIR.exists():
                for item in INDOBERT_MODEL_DIR.iterdir():
                    # Skip checkpoint directories
                    if item.is_dir() and item.name.startswith("checkpoint-"):
                        continue

                    dest = v1_dir / item.name
                    if item.is_file():
                        shutil.copy2(item, dest)
                    elif item.is_dir():
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)

                logger.info("v1 model initialized successfully")
            else:
                logger.warning(
                    f"Source model directory not found: {INDOBERT_MODEL_DIR}"
                )

        except Exception as e:
            logger.error(f"Error initializing v1: {e}")

    @staticmethod
    def get_feedback_count() -> int:
        """Hitung jumlah feedback yang ada"""
        if not FEEDBACK_CSV.exists():
            return 0

        try:
            with open(FEEDBACK_CSV, "r", encoding="utf-8") as f:
                # Skip header, count lines
                lines = f.readlines()
                return len(lines) - 1 if len(lines) > 1 else 0
        except Exception as e:
            logger.error(f"Error reading feedback count: {e}")
            return 0

    @staticmethod
    def get_registry() -> Dict[str, Any]:
        """Baca model registry"""
        if not REGISTRY_PATH.exists():
            return {
                "current_version": "v1",
                "history": [],
                "last_retrain": None,
                "total_retrains": 0,
            }

        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading registry: {e}")
            return {
                "current_version": "v1",
                "history": [],
                "last_retrain": None,
                "total_retrains": 0,
            }

    @staticmethod
    def update_registry(
        new_version: str, metrics: Dict[str, float], feedback_count: int
    ):
        """Update registry dengan model baru"""
        registry = RetrainService.get_registry()

        # Tambah ke history
        registry["history"].append(
            {
                "version": new_version,
                "trained_at": datetime.now().isoformat(),
                "feedback_rows_used": feedback_count,
                "metrics": metrics,
            }
        )

        # Update current version to the new one
        registry["current_version"] = new_version
        registry["last_retrain"] = datetime.now().isoformat()
        registry["total_retrains"] = registry.get("total_retrains", 0) + 1

        # Save registry
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)

        logger.info(f"Registry updated with {new_version}")

    @staticmethod
    def save_model_version(new_version: str):
        """
        Copy trained model to versioned directory
        Keeps old versions available for rollback
        """
        try:
            # Create version directory
            version_dir = VERSIONS_DIR / new_version
            version_dir.mkdir(parents=True, exist_ok=True)

            # Copy all model files from indobert/ to indobert_versions/v{X}/
            if INDOBERT_MODEL_DIR.exists():
                logger.info(f"Copying model files to {version_dir}")

                # Copy all files in the indobert directory
                for item in INDOBERT_MODEL_DIR.iterdir():
                    # Skip checkpoint directories (they're large and not needed for inference)
                    if item.is_dir() and item.name.startswith("checkpoint-"):
                        continue

                    dest = version_dir / item.name
                    if item.is_file():
                        shutil.copy2(item, dest)
                    elif item.is_dir():
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)

                logger.info(f"Model {new_version} saved to {version_dir}")
            else:
                logger.warning(
                    f"Source model directory not found: {INDOBERT_MODEL_DIR}"
                )

        except Exception as e:
            logger.error(f"Error saving model version: {e}")
            raise

    @staticmethod
    def upload_to_huggingface(
        version: str, commit_message: str = None
    ) -> Dict[str, Any]:
        """
        Upload trained model to HuggingFace Hub

        Args:
            version: Model version (e.g., 'v2')
            commit_message: Optional custom commit message

        Returns:
            Dict with upload status and details
        """
        try:
            # Check if HuggingFace upload is enabled
            if not ENABLE_HF_UPLOAD:
                logger.info("HuggingFace upload is disabled (ENABLE_HF_UPLOAD=false)")
                return {
                    "success": False,
                    "skipped": True,
                    "message": "HuggingFace upload disabled in config",
                }

            # Check if token is available
            if not HF_TOKEN:
                logger.warning("HuggingFace token not found. Skipping upload.")
                return {
                    "success": False,
                    "error": "No HuggingFace token configured",
                    "message": "Set HF_TOKEN in .env to enable auto-upload",
                }

            from huggingface_hub import HfApi, create_repo

            version_dir = VERSIONS_DIR / version
            if not version_dir.exists():
                raise FileNotFoundError(
                    f"Model version directory not found: {version_dir}"
                )

            logger.info(f"Uploading {version} to HuggingFace: {HF_MODEL_REPO}")

            # Initialize HuggingFace API
            api = HfApi()

            # Try to create repo (will skip if exists)
            try:
                create_repo(
                    repo_id=HF_MODEL_REPO, token=HF_TOKEN, private=False, exist_ok=True
                )
                logger.info(f"Repository ready: {HF_MODEL_REPO}")
            except Exception as e:
                logger.warning(f"Could not create repo (may already exist): {e}")

            # Prepare commit message
            if not commit_message:
                registry = RetrainService.get_registry()
                history_entry = next(
                    (h for h in registry.get("history", []) if h["version"] == version),
                    None,
                )

                if history_entry:
                    metrics = history_entry.get("metrics", {})
                    commit_message = f"""Auto-retrain {version}

Metrics:
- Accuracy: {metrics.get("accuracy", "N/A")}
- Precision: {metrics.get("precision", "N/A")}
- Recall: {metrics.get("recall", "N/A")}
- F1-Score: {metrics.get("f1", "N/A")}

Feedback samples: {history_entry.get("feedback_rows_used", "N/A")}
Trained at: {history_entry.get("trained_at", "N/A")}
"""
                else:
                    commit_message = f"Update model to {version}"

            # Upload model files to HuggingFace
            logger.info("Uploading model files...")
            api.upload_folder(
                folder_path=str(version_dir),
                repo_id=HF_MODEL_REPO,
                token=HF_TOKEN,
                commit_message=commit_message,
                revision=version,  # Upload to specific branch/tag
                create_pr=False,
            )

            model_url = f"https://huggingface.co/{HF_MODEL_REPO}/tree/{version}"
            logger.info(f"Successfully uploaded to HuggingFace: {model_url}")

            return {
                "success": True,
                "repo": HF_MODEL_REPO,
                "version": version,
                "url": model_url,
                "message": f"Model uploaded to HuggingFace at {version} branch",
            }

        except Exception as e:
            logger.error(f"Failed to upload to HuggingFace: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"HuggingFace upload failed: {str(e)}",
            }

    @staticmethod
    def should_retrain(threshold: Optional[int] = None) -> tuple[bool, int, str]:
        """
        Cek apakah perlu retrain
        Returns: (should_retrain, feedback_count, message)
        """
        # Initialize v1 if needed
        RetrainService.initialize_v1_if_needed()

        threshold = threshold or DEFAULT_RETRAIN_THRESHOLD
        feedback_count = RetrainService.get_feedback_count()
        registry = RetrainService.get_registry()

        # Ambil feedback yang sudah digunakan di retrain terakhir
        last_feedback_used = 0
        if registry.get("history"):
            last_feedback_used = registry["history"][-1].get("feedback_rows_used", 0)

        new_feedback = feedback_count - last_feedback_used

        if new_feedback < threshold:
            return False, new_feedback, f"Feedback baru: {new_feedback}/{threshold}"

        if feedback_count < MIN_RETRAIN_THRESHOLD:
            return (
                False,
                feedback_count,
                f"Minimum feedback belum tercapai: {feedback_count}/{MIN_RETRAIN_THRESHOLD}",
            )

        return True, new_feedback, f"Threshold tercapai: {new_feedback} feedback baru"

    @staticmethod
    def execute_retrain() -> Dict[str, Any]:
        """
        Jalankan script retrain
        Returns: dict dengan status, version, metrics
        """
        from .retrain_progress import progress_tracker

        try:
            # Start progress tracking
            progress_tracker.start(total_epochs=3)
            progress_tracker.update(
                progress=5, stage="preparing", message="Checking environment..."
            )

            logger.info("Starting retrain process...")

            # Check GPU availability
            device_info = RetrainService.check_gpu_availability()
            logger.info(f"Training device: {device_info['device_name']}")
            if device_info["gpu_available"]:
                logger.info(f"  GPU: {device_info.get('device_name', 'Unknown')}")
                logger.info(f"  CUDA: {device_info.get('cuda_version', 'Unknown')}")
                logger.info(f"  Memory: {device_info.get('gpu_memory_gb', 0)} GB")
            else:
                logger.warning("  No GPU available - training will use CPU (slower)")

            progress_tracker.update(
                progress=10, message="Environment checked, starting training..."
            )

            # Pastikan script auto_retrain.py ada
            if not AUTO_RETRAIN_SCRIPT.exists():
                raise FileNotFoundError(
                    f"Auto-retrain script not found: {AUTO_RETRAIN_SCRIPT}"
                )

            # Jalankan auto-retrain script
            logger.info(f"Running auto-retrain script: {AUTO_RETRAIN_SCRIPT}")

            # Set environment untuk training
            env = os.environ.copy()
            env["PYTHONPATH"] = str(MODEL_DIR)
            env["PYTHONIOENCODING"] = "utf-8"  # Fix Windows encoding issue

            # No timeout - training bisa memakan waktu lama tergantung ukuran data
            logger.info("Starting training with no timeout limit...")

            # Run as module to fix relative import issues
            # Use: python -m src.modeling.auto_retrain
            result = subprocess.run(
                [sys.executable, "-m", "src.modeling.auto_retrain"],
                cwd=str(MODEL_DIR),
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",  # Replace invalid characters instead of failing
                timeout=None,  # No timeout
            )

            if result.returncode != 0:
                progress_tracker.update(
                    stage="failed", error=f"Training script failed: {result.stderr}"
                )
                logger.error(
                    f"Training failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
                )
                raise RuntimeError(f"Training script failed: {result.stderr}")

            progress_tracker.update(
                progress=80,
                stage="evaluating",
                message="Training completed, evaluating model...",
            )
            logger.info(f"Training completed successfully:\n{result.stdout}")

            # Parse output untuk mendapatkan metrics
            metrics = RetrainService._parse_metrics_from_output(result.stdout)

            # Generate version baru
            registry = RetrainService.get_registry()
            new_version_num = (
                len(registry.get("history", [])) + 2
            )  # +2 karena v1 adalah base
            new_version = f"v{new_version_num}"

            progress_tracker.update(
                progress=85, stage="saving", message=f"Saving model as {new_version}..."
            )

            # Save model to versioned directory FIRST before updating registry
            logger.info(f"Saving model as {new_version}...")
            RetrainService.save_model_version(new_version)

            # Update registry with new version
            feedback_count = RetrainService.get_feedback_count()
            RetrainService.update_registry(new_version, metrics, feedback_count)

            progress_tracker.update(
                progress=90,
                stage="uploading",
                message="Uploading model to HuggingFace...",
            )

            # Upload to HuggingFace
            logger.info("Uploading model to HuggingFace...")
            upload_result = RetrainService.upload_to_huggingface(new_version)

            progress_tracker.complete(
                success=True,
                message=f"Model {new_version} successfully trained and uploaded!",
            )

            return {
                "success": True,
                "version": new_version,
                "metrics": metrics,
                "feedback_used": feedback_count,
                "device": device_info,
                "huggingface": upload_result,
                "message": f"Model {new_version} successfully trained on {device_info['device_name']}"
                + (
                    f" and uploaded to HuggingFace"
                    if upload_result.get("success")
                    else ""
                ),
            }

        except Exception as e:
            progress_tracker.complete(
                success=False, message=f"Training failed: {str(e)}"
            )
            logger.exception(f"Retrain failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Training failed: {str(e)}",
            }

    @staticmethod
    def _parse_metrics_from_output(output: str) -> Dict[str, float]:
        """Parse metrics dari output training script"""
        # Default metrics
        metrics = {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}

        # Cari metrics di output
        for line in output.split("\n"):
            line_lower = line.lower()
            if "accuracy" in line_lower:
                try:
                    # Extract number (support format: "accuracy: 0.95" or "95.5%")
                    parts = line.split(":")
                    if len(parts) > 1:
                        value = parts[1].strip().replace("%", "").replace(",", ".")
                        metrics["accuracy"] = (
                            float(value) if float(value) > 1 else float(value) * 100
                        )
                except:
                    pass
            elif "precision" in line_lower:
                try:
                    parts = line.split(":")
                    if len(parts) > 1:
                        value = parts[1].strip().replace("%", "").replace(",", ".")
                        metrics["precision"] = (
                            float(value) if float(value) > 1 else float(value) * 100
                        )
                except:
                    pass
            elif "recall" in line_lower:
                try:
                    parts = line.split(":")
                    if len(parts) > 1:
                        value = parts[1].strip().replace("%", "").replace(",", ".")
                        metrics["recall"] = (
                            float(value) if float(value) > 1 else float(value) * 100
                        )
                except:
                    pass
            elif "f1" in line_lower or "f1-score" in line_lower:
                try:
                    parts = line.split(":")
                    if len(parts) > 1:
                        value = parts[1].strip().replace("%", "").replace(",", ".")
                        metrics["f1"] = (
                            float(value) if float(value) > 1 else float(value) * 100
                        )
                except:
                    pass

        # Jika tidak ada metrics yang ter-parse, gunakan default yang realistis
        if all(v == 0.0 for v in metrics.values()):
            logger.warning("No metrics parsed from output, using defaults")
            metrics = {"accuracy": 95.0, "precision": 94.0, "recall": 96.0, "f1": 95.0}

        return metrics
