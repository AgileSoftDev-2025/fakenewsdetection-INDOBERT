from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException
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
async def patch_feedback(row_id: int, body: FeedbackUpdateRequest):
    try:
        ok = update_user_label(row_id, int(body.user_label))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {e}")
    if not ok:
        raise HTTPException(status_code=404, detail="Row not found")
    return {"updated": True}
