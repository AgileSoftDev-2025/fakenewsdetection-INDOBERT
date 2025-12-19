from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Use stub in Railway production
try:
    from src.services.model_registry import (
        get_current_version,
        _read_registry,
        _write_registry,
    )  # type: ignore
except ModuleNotFoundError:
    from ..services.model_registry_stub import (
        get_current_version,
        _read_registry,
        _write_registry,
    )

router = APIRouter()


class VersionResponse(BaseModel):
    version: str


class ModelInfo(BaseModel):
    id: int
    name: str
    description: str
    version: str
    metrics: Dict[str, float]


class ActiveModelResponse(BaseModel):
    active_model: str
    metrics: Dict[str, float]


class ActivateModelRequest(BaseModel):
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


@router.get("/api/models", response_model=List[ModelInfo])
async def get_models() -> List[ModelInfo]:
    """Get all available models with their metrics"""
    try:
        registry = _read_registry()
        history = registry.get("history", [])

        models = []

        # Add current/base model (v1)
        models.append(
            ModelInfo(
                id=1,
                name="IndoBERT Base Model",
                description="Model dasar IndoBERT untuk deteksi berita hoax",
                version="v1",
                metrics={
                    "accuracy": 95.0,
                    "precision": 94.0,
                    "recall": 96.0,
                    "f1": 95.0,
                },
            )
        )

        # Add models from history
        for idx, entry in enumerate(history, start=2):
            version = entry.get("version", f"v{idx}")
            metrics_data = entry.get("metrics", {})

            # Extract metrics with defaults
            metrics = {
                "accuracy": round(metrics_data.get("accuracy", 0.0) * 100, 1)
                if metrics_data.get("accuracy", 0) <= 1
                else round(metrics_data.get("accuracy", 0.0), 1),
                "precision": round(metrics_data.get("precision", 0.0) * 100, 1)
                if metrics_data.get("precision", 0) <= 1
                else round(metrics_data.get("precision", 0.0), 1),
                "recall": round(metrics_data.get("recall", 0.0) * 100, 1)
                if metrics_data.get("recall", 0) <= 1
                else round(metrics_data.get("recall", 0.0), 1),
                "f1": round(metrics_data.get("f1", 0.0) * 100, 1)
                if metrics_data.get("f1", 0) <= 1
                else round(metrics_data.get("f1", 0.0), 1),
            }

            models.append(
                ModelInfo(
                    id=idx,
                    name=f"IndoBERT {version}",
                    description=f"Model retrained dengan {entry.get('feedback_rows_used', 0)} feedback",
                    version=version,
                    metrics=metrics,
                )
            )

        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading models: {str(e)}")


@router.get("/api/models/active", response_model=ActiveModelResponse)
async def get_active_model() -> ActiveModelResponse:
    """Get currently active model version with metrics"""
    try:
        registry = _read_registry()
        current = registry.get("current_version", "v1")

        # Get metrics for current model
        metrics = {
            "accuracy": 95.0,
            "precision": 94.0,
            "recall": 96.0,
            "f1": 95.0,
        }

        # If not v1, get metrics from history
        if current != "v1":
            history = registry.get("history", [])
            for entry in history:
                if entry.get("version") == current:
                    metrics_data = entry.get("metrics", {})
                    metrics = {
                        "accuracy": round(metrics_data.get("accuracy", 0.0) * 100, 1)
                        if metrics_data.get("accuracy", 0) <= 1
                        else round(metrics_data.get("accuracy", 0.0), 1),
                        "precision": round(metrics_data.get("precision", 0.0) * 100, 1)
                        if metrics_data.get("precision", 0) <= 1
                        else round(metrics_data.get("precision", 0.0), 1),
                        "recall": round(metrics_data.get("recall", 0.0) * 100, 1)
                        if metrics_data.get("recall", 0) <= 1
                        else round(metrics_data.get("recall", 0.0), 1),
                        "f1": round(metrics_data.get("f1", 0.0) * 100, 1)
                        if metrics_data.get("f1", 0) <= 1
                        else round(metrics_data.get("f1", 0.0), 1),
                    }
                    break

        return ActiveModelResponse(active_model=current, metrics=metrics)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting active model: {str(e)}"
        )


@router.post("/api/models/{version}/activate")
async def activate_model(version: str) -> Dict[str, Any]:
    """Activate a specific model version"""
    try:
        registry = _read_registry()

        # Validate version exists
        if version == "v1":
            # v1 is always valid (base model)
            pass
        else:
            history = registry.get("history", [])
            versions = [entry.get("version") for entry in history]
            if version not in versions:
                raise HTTPException(
                    status_code=404, detail=f"Model version {version} not found"
                )

        # Update current version
        registry["current_version"] = version
        _write_registry(registry)

        return {
            "success": True,
            "active_model": version,
            "message": f"Model {version} activated",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error activating model: {str(e)}")


@router.post("/api/models/deactivate")
async def deactivate_model() -> Dict[str, Any]:
    """Deactivate current model (set to v1 as default)"""
    try:
        registry = _read_registry()
        registry["current_version"] = "v1"
        _write_registry(registry)

        return {
            "success": True,
            "active_model": "v1",
            "message": "Model deactivated, using v1",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deactivating model: {str(e)}"
        )


@router.get("/admin/stats", response_model=StatsResponse)
async def get_stats() -> StatsResponse:
    """
    Get statistics from database or CSV fallback
    Returns total checks, hoax count, valid count, and percentages
    """
    try:
        # Check if database mode is enabled
        use_database = os.getenv("USE_DATABASE", "false").lower() == "true"

        if use_database:
            # Import and create database session only when needed
            from app.database import SessionLocal
            from app.models import Feedback as FeedbackModel

            db = SessionLocal()
            try:
                # Get stats from database
                total = db.query(FeedbackModel).count()
                hoax_count = (
                    db.query(FeedbackModel)
                    .filter(FeedbackModel.prediction == 1)
                    .count()
                )
                valid_count = (
                    db.query(FeedbackModel)
                    .filter(FeedbackModel.prediction == 0)
                    .count()
                )
            finally:
                db.close()
        else:
            # Fallback to CSV (for development)
            feedback_path = (
                Path(__file__).resolve().parents[4]
                / "Model IndoBERT"
                / "data"
                / "feedback"
                / "feedback.csv"
            )

            if not feedback_path.exists():
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
