from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.services.model_registry import get_current_version  # type: ignore

router = APIRouter()


class VersionResponse(BaseModel):
    version: str


@router.get("/model/version", response_model=VersionResponse)
async def model_version() -> VersionResponse:
    try:
        ver = get_current_version()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registry error: {e}")
    return VersionResponse(version=ver)
