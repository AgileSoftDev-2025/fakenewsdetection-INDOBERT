from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import json, uuid, logging
from pathlib import Path
from datetime import datetime

router = APIRouter(tags=["results"])
logger = logging.getLogger(__name__)

# Buat folder untuk nyimpen hasil
RESULTS_DIR = Path("data/shared_results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

class ResultCreate(BaseModel):
    title: Optional[str] = None
    text: str
    prediction: int
    prob_hoax: float
    model_version: str
    extracted_text: Optional[str] = None

class ResultResponse(BaseModel):
    id: str
    # ✅ HAPUS field "url" - biar frontend yang generate

class ResultDetail(BaseModel):
    id: str
    title: Optional[str]
    text: str
    prediction: int
    prob_hoax: float
    model_version: str
    extracted_text: Optional[str]
    created_at: str

@router.post("/results", response_model=ResultResponse)
async def create_shared_result(data: ResultCreate):
    """Simpan hasil analisis dan return ID"""
    result_id = str(uuid.uuid4())[:12]
    
    result_data = {
        "id": result_id,
        "title": data.title,
        "text": data.text,
        "prediction": data.prediction,
        "prob_hoax": data.prob_hoax,
        "model_version": data.model_version,
        "extracted_text": data.extracted_text,
        "created_at": datetime.now().isoformat()
    }
    
    # Simpan ke file JSON
    result_file = RESULTS_DIR / f"{result_id}.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ Saved result with ID: {result_id}")
    
    # ✅ Return cuma ID, URL dibuat di frontend
    return {"id": result_id}

@router.get("/results/{result_id}", response_model=ResultDetail)
async def get_shared_result(result_id: str):
    """Ambil hasil analisis berdasarkan ID"""
    result_file = RESULTS_DIR / f"{result_id}.json"
    
    if not result_file.exists():
        logger.warning(f"❌ Result not found: {result_id}")
        raise HTTPException(status_code=404, detail="Result not found")
    
    logger.info(f"✅ Fetched result: {result_id}")
    
    with open(result_file, "r", encoding="utf-8") as f:
        return json.load(f)
