from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from src.feedback import update_user_label, iter_feedback  # type: ignore

router = APIRouter()


class FeedbackUpdateRequest(BaseModel):
    user_label: int  # 0 or 1


class FeedbackItem(BaseModel):
    model_config = {"protected_namespaces": ()}
    id: int
    timestamp: int
    model_name: str
    model_version: str
    prediction: int
    prob_hoax: float
    user_label: Optional[int] = None
    agreement: str
    text_length: int


@router.get("/feedback", response_model=List[FeedbackItem])
async def list_feedback(limit: int = 50) -> List[FeedbackItem]:
    try:
        rows = iter_feedback(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Read feedback failed: {e}")
    out: List[FeedbackItem] = []
    for r in rows:
        out.append(
            FeedbackItem(
                id=int(r["id"]),
                timestamp=int(r["timestamp"]),
                model_name=r.get("model_name", ""),
                model_version=r.get("model_version", ""),
                prediction=int(r.get("prediction", 0)),
                prob_hoax=float(r.get("prob_hoax", 0.0)),
                user_label=None
                if r.get("user_label", "") == ""
                else int(r["user_label"]),
                agreement=r.get("agreement", "unknown"),
                text_length=int(r.get("text_length", 0)),
            )
        )
    return out


@router.patch("/feedback/{row_id}")
async def patch_feedback(
    row_id: int, body: FeedbackUpdateRequest, background_tasks: BackgroundTasks
):
    try:
        ok = update_user_label(row_id, int(body.user_label))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {e}")
    if not ok:
        raise HTTPException(status_code=404, detail="Row not found")

    # Auto-check untuk retrain setelah feedback di-update
    background_tasks.add_task(_check_and_trigger_retrain)

    return {"updated": True}


def _check_and_trigger_retrain():
    """Background task untuk cek dan trigger retrain jika perlu"""
    try:
        from ..services.retrain_service import RetrainService
        import logging

        logger = logging.getLogger(__name__)

        should_retrain, new_feedback, message = RetrainService.should_retrain()

        if should_retrain:
            logger.info(f"🔄 Auto-retrain triggered: {message}")
            result = RetrainService.execute_retrain()

            if result["success"]:
                logger.info(f"✅ Auto-retrain completed: {result['version']}")
            else:
                logger.error(f"❌ Auto-retrain failed: {result.get('error')}")
        else:
            logger.debug(f"⏭️ Auto-retrain skipped: {message}")

    except Exception as e:
        import logging

        logging.getLogger(__name__).exception(f"Error in auto-retrain check: {e}")
