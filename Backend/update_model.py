from __future__ import annotations

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Dummy Database
dummy_db = {
    "models": [
        {
            "id": 1,
            "name": "ML Model",
            "version": "v1.0",
            "description": "Stable release for production",
            "metrics": {"accuracy": 89, "precision": 84, "recall": 87, "f1": 86},
        },
        {
            "id": 2,
            "name": "ML Model",
            "version": "v2.0",
            "description": "Improved contextual accuracy",
            "metrics": {"accuracy": 91, "precision": 90, "recall": 88, "f1": 89},
        },
        {
            "id": 3,
            "name": "ML Model",
            "version": "v3.0",
            "description": "Added linguistic normalization features",
            "metrics": {"accuracy": 93, "precision": 92, "recall": 91, "f1": 92},
        },
        {
            "id": 4,
            "name": "ML Model",
            "version": "v4.0",
            "description": "Enhanced IndoBERT fine-tuning",
            "metrics": {"accuracy": 95, "precision": 94, "recall": 93, "f1": 94},
        },
    ],
    "active_model": "v1.0",
}

# Data Classes

class Metrics(BaseModel):
    accuracy: int
    precision: int
    recall: int
    f1: int


class ModelItem(BaseModel):
    model_config = {"protected_namespaces": ()}
    id: int
    name: str
    version: str
    description: str
    metrics: Metrics


class ActivateResponse(BaseModel):
    message: str
    active_model: Optional[str]


class ActiveModelResponse(BaseModel):
    active_model: Optional[str]


# Route

@router.get("/models", response_model=List[ModelItem])
async def list_models():
    """Return list of all model versions."""
    return dummy_db["models"]


@router.get("/models/active", response_model=ActiveModelResponse)
async def get_active_model():
    """Return currently active model version."""
    return {"active_model": dummy_db["active_model"]}


@router.post("/models/{version}/activate", response_model=ActivateResponse)
async def activate_model(version: str):
    """Activate model by version."""
    versions = [m["version"] for m in dummy_db["models"]]

    if version not in versions:
        raise HTTPException(status_code=404, detail="Model not found")

    dummy_db["active_model"] = version
    return {"message": f"Model changed to {version}", "active_model": version}


@router.post("/models/deactivate", response_model=ActivateResponse)
async def deactivate_model():
    """Deactivate currently active model."""
    dummy_db["active_model"] = None
    return {"message": "Model deactivated", "active_model": None}
