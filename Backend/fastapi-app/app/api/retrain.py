"""
API endpoints for model retraining management.
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from ..services.retrain_service import RetrainService
from ..services.retrain_progress import progress_tracker

logger = logging.getLogger(__name__)

router = APIRouter()


class RetrainStatusResponse(BaseModel):
    should_retrain: bool
    new_feedback_count: int
    message: str
    threshold: int
    total_feedback: int


class RetrainProgressResponse(BaseModel):
    is_running: bool
    progress: int  # 0-100
    stage: str
    message: str
    started_at: Optional[float] = None
    estimated_completion: Optional[float] = None
    current_epoch: int
    total_epochs: int
    error: Optional[str] = None


class RetrainTriggerResponse(BaseModel):
    success: bool
    message: str
    is_background: bool
    status: Optional[str] = None


class RetrainResultResponse(BaseModel):
    success: bool
    version: Optional[str] = None
    metrics: Optional[Dict[str, float]] = None
    feedback_used: Optional[int] = None
    message: str
    error: Optional[str] = None


@router.get("/retrain/status", response_model=RetrainStatusResponse)
async def check_retrain_status(threshold: Optional[int] = None):
    """
    Cek apakah model perlu di-retrain berdasarkan jumlah feedback.

    - **threshold**: Custom threshold (opsional, default dari env RETRAIN_THRESHOLD)
    """
    try:
        should_retrain, new_feedback, message = RetrainService.should_retrain(threshold)
        total_feedback = RetrainService.get_feedback_count()

        return RetrainStatusResponse(
            should_retrain=should_retrain,
            new_feedback_count=new_feedback,
            message=message,
            threshold=threshold or 100,
            total_feedback=total_feedback,
        )
    except Exception as e:
        logger.exception(f"Error checking retrain status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/retrain/trigger", response_model=RetrainTriggerResponse)
async def trigger_retrain(
    background_tasks: BackgroundTasks, force: bool = False, background: bool = True
):
    """
    Trigger model retraining.

    - **force**: Paksa retrain meskipun threshold belum tercapai
    - **background**: Jalankan di background (recommended)

    Returns status dan job ID jika background=True
    """
    try:
        # Cek apakah perlu retrain
        if not force:
            should_retrain, new_feedback, message = RetrainService.should_retrain()

            if not should_retrain:
                return RetrainTriggerResponse(
                    success=False,
                    message=f"Retrain tidak diperlukan. {message}",
                    is_background=False,
                    status="skipped",
                )

        # Jalankan retrain
        if background:
            # Background task
            background_tasks.add_task(_execute_retrain_background)

            return RetrainTriggerResponse(
                success=True,
                message="Retrain job dimulai di background. Cek logs untuk progress.",
                is_background=True,
                status="started",
            )
        else:
            # Synchronous (blocking)
            logger.info("Starting synchronous retrain...")
            result = RetrainService.execute_retrain()

            return RetrainTriggerResponse(
                success=result["success"],
                message=result["message"],
                is_background=False,
                status="completed" if result["success"] else "failed",
            )

    except Exception as e:
        logger.exception(f"Error triggering retrain: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/retrain/history")
async def get_retrain_history():
    """Get history of all retrain operations"""
    try:
        registry = RetrainService.get_registry()

        return {
            "total_retrains": registry.get("total_retrains", 0),
            "last_retrain": registry.get("last_retrain"),
            "current_version": registry.get("current_version", "v1"),
            "history": registry.get("history", []),
        }
    except Exception as e:
        logger.exception(f"Error getting retrain history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/retrain/progress", response_model=RetrainProgressResponse)
async def get_retrain_progress():
    """Get current retrain progress"""
    try:
        state = progress_tracker.get_state()

        return RetrainProgressResponse(
            is_running=state["is_running"],
            progress=state["progress"],
            stage=state["stage"],
            message=state["message"],
            started_at=state.get("started_at"),
            estimated_completion=state.get("estimated_completion"),
            current_epoch=state["current_epoch"],
            total_epochs=state["total_epochs"],
            error=state.get("error"),
        )
    except Exception as e:
        logger.exception(f"Error getting retrain progress: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/retrain/reset")
async def reset_retrain_progress():
    """Reset retrain progress to idle state (admin only)"""
    try:
        progress_tracker.reset()
        logger.info("Retrain progress has been reset to idle state")
        return {
            "success": True,
            "message": "Retrain progress berhasil direset",
        }
    except Exception as e:
        logger.exception(f"Error resetting retrain progress: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/retrain/start")
async def start_retrain_manual(background_tasks: BackgroundTasks):
    """
    Start manual retrain (admin only).
    This will start retrain in background regardless of feedback count.
    """
    try:
        # Check if already running
        state = progress_tracker.get_state()
        if state.get("is_running"):
            return {
                "success": False,
                "message": "Retrain sudah sedang berjalan. Tunggu hingga selesai atau reset progress terlebih dahulu.",
            }

        # Start background retrain
        background_tasks.add_task(_execute_retrain_background)

        logger.info("Manual retrain started by admin")
        return {
            "success": True,
            "message": "Retrain berhasil dimulai. Proses berjalan di background.",
        }
    except Exception as e:
        logger.exception(f"Error starting manual retrain: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _execute_retrain_background():
    """Background task untuk retrain"""
    try:
        logger.info("⚙️ Background retrain started...")
        result = RetrainService.execute_retrain()

        if result["success"]:
            logger.info(f"✅ Background retrain completed: {result['version']}")
            logger.info(f"📊 Metrics: {result['metrics']}")
        else:
            logger.error(f"❌ Background retrain failed: {result.get('error')}")

    except Exception as e:
        logger.exception(f"❌ Background retrain exception: {e}")
