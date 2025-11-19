from __future__ import annotations

from typing import Any, Dict
import csv
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.services.model_registry import get_current_version  # type: ignore

router = APIRouter()


class VersionResponse(BaseModel):
    version: str


class StatsResponse(BaseModel):
    total: int
    hoax: int
    valid: int
    hoax_percentage: float
    valid_percentage: float


@router.get("/model/version", response_model=VersionResponse)
async def model_version() -> VersionResponse:
    try:
        ver = get_current_version()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registry error: {e}")
    return VersionResponse(version=ver)


@router.get("/admin/stats", response_model=StatsResponse)
async def get_stats() -> StatsResponse:
    """
    Get statistics from feedback.csv
    Returns total checks, hoax count, valid count, and percentages
    """
    try:
        # Path to feedback.csv
        feedback_path = (
            Path(__file__).resolve().parents[4]
            / "Model IndoBERT"
            / "data"
            / "feedback"
            / "feedback.csv"
        )

        if not feedback_path.exists():
            # Return default values if file doesn't exist
            return StatsResponse(
                total=0, hoax=0, valid=0, hoax_percentage=0.0, valid_percentage=0.0
            )

        # Read CSV and count statistics
        total = 0
        hoax_count = 0
        valid_count = 0

        with open(feedback_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                # prediction: 1 = hoax, 0 = valid
                if row.get("prediction") == "1":
                    hoax_count += 1
                else:
                    valid_count += 1

        # Calculate percentages
        hoax_percentage = round((hoax_count / total * 100), 1) if total > 0 else 0.0
        valid_percentage = round((valid_count / total * 100), 1) if total > 0 else 0.0

        return StatsResponse(
            total=total,
            hoax=hoax_count,
            valid=valid_count,
            hoax_percentage=hoax_percentage,
            valid_percentage=valid_percentage,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading stats: {str(e)}")
