from __future__ import annotations

from typing import Optional
from io import BytesIO
import os
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from pydantic import BaseModel

# Import project functions
# Use stub in Railway production (no Model IndoBERT folder available)
try:
    from src.services.model_registry import get_current_version  # type: ignore
except ModuleNotFoundError:
    from ..services.model_registry_stub import get_current_version

from ..services.hf_space_service import HFSpaceService

router = APIRouter()


class PredictRequest(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    body: Optional[str] = None
    log_feedback: bool = True
    user_label: Optional[int] = None  # 0/1


class PredictResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    prediction: int
    prob_hoax: float
    model_version: str


class PredictFileResponse(PredictResponse):
    extracted_text: str


@router.post("/predict", response_model=PredictResponse)
async def predict(
    req: PredictRequest, background_tasks: BackgroundTasks
) -> PredictResponse:
    # Build text from fields
    text = (req.text or "").strip()
    if not text:
        title = (req.title or "").strip()
        body = (req.body or "").strip()
        text = (title + "\n\n" + body).strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text/title/body is required")

    # Call HuggingFace Space with fallback to local model
    try:
        result = await HFSpaceService.predict_with_fallback(
            text,
            user_label=req.user_label,
            log_feedback=req.log_feedback,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")

    if not result.get("success"):
        raise HTTPException(
            status_code=500, detail=result.get("error", "Unknown prediction error")
        )

    # Auto-check untuk retrain setelah prediksi
    if req.log_feedback:
        background_tasks.add_task(_check_and_trigger_retrain)

    return PredictResponse(
        prediction=int(result["prediction"]),
        prob_hoax=float(result["prob_hoax"]),
        model_version=result.get("model_version", get_current_version()),
    )


@router.post("/predict-file", response_model=PredictFileResponse)
async def predict_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PNG/JPG gambar atau DOCX dokumen"),
    log_feedback: bool = True,
    user_label: Optional[int] = None,
) -> PredictFileResponse:
    data = await file.read()
    content_type = (file.content_type or "").lower()
    name = (file.filename or "").lower()

    text = ""

    is_image = content_type in {
        "image/png",
        "image/jpeg",
        "image/jpg",
    } or name.endswith((".png", ".jpg", ".jpeg"))
    is_docx = content_type in {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    } or name.endswith(".docx")

    if not (is_image or is_docx):
        raise HTTPException(
            status_code=400, detail="Format tidak didukung. Gunakan PNG/JPG atau DOCX."
        )

    if is_docx:
        # Parse DOCX text
        try:
            from docx import Document  # type: ignore

            doc = Document(BytesIO(data))
            text = "\n".join([p.text for p in doc.paragraphs]).strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Gagal membaca DOCX: {e}")
    else:
        # Image OCR path
        try:
            from PIL import Image
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Pillow tidak tersedia: {e}")

        try:
            image = Image.open(BytesIO(data)).convert("L")  # grayscale ringan
        except Exception:
            raise HTTPException(
                status_code=400, detail="Gagal membaca gambar. Pastikan file valid."
            )

        # Run OCR via pytesseract
        try:
            import pytesseract

            # Configure tesseract path on Windows if available
            tess_cmd = os.environ.get("TESSERACT_CMD")
            if tess_cmd:
                pytesseract.pytesseract.tesseract_cmd = tess_cmd
            else:
                default_win = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
                if os.name == "nt" and Path(default_win).exists():
                    pytesseract.pytesseract.tesseract_cmd = default_win
            try:
                # Try Indonesian + English; fall back to default if not installed
                text = pytesseract.image_to_string(image, lang="ind+eng")
                if not text.strip():
                    text = pytesseract.image_to_string(image)
            except pytesseract.TesseractError:
                text = pytesseract.image_to_string(image)
        except ImportError:
            raise HTTPException(
                status_code=500,
                detail=(
                    "OCR tidak aktif: pustaka pytesseract belum terpasang atau biner Tesseract belum tersedia. "
                    "Install dengan 'pip install pytesseract' dan pasang Tesseract OCR (Windows: https://github.com/UB-Mannheim/tesseract/wiki)."
                ),
            )

    text = text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Teks tidak terbaca dari file.")

    # Use HF Space (with fallback) for the extracted text
    try:
        result = await HFSpaceService.predict_with_fallback(
            text,
            user_label=user_label,
            log_feedback=log_feedback,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")

    if not result.get("success"):
        raise HTTPException(
            status_code=500, detail=result.get("error", "Unknown prediction error")
        )

    # Auto-check untuk retrain setelah prediksi
    if log_feedback:
        background_tasks.add_task(_check_and_trigger_retrain)

    return PredictFileResponse(
        prediction=int(result["prediction"]),
        prob_hoax=float(result["prob_hoax"]),
        model_version=result.get("model_version", get_current_version()),
        extracted_text=text,
    )


def _check_and_trigger_retrain():
    """Background task untuk cek dan trigger retrain jika perlu"""
    try:
        import sys
        from pathlib import Path

        # Add services to path
        backend_path = Path(__file__).resolve().parents[1]
        if str(backend_path) not in sys.path:
            sys.path.insert(0, str(backend_path))

        from services.retrain_service import RetrainService
        import logging

        logger = logging.getLogger(__name__)

        should_retrain, new_feedback, message = RetrainService.should_retrain()

        if should_retrain:
            logger.info(f"🔄 Auto-retrain triggered: {message}")
            result = RetrainService.execute_retrain()

            if result["success"]:
                logger.info(f"✅ Auto-retrain completed: {result['version']}")
                logger.info(f"📊 Metrics: {result['metrics']}")
            else:
                logger.error(f"❌ Auto-retrain failed: {result.get('error')}")
        else:
            logger.debug(f"⏭️ Auto-retrain skipped: {message}")

    except Exception as e:
        import logging

        logging.getLogger(__name__).exception(f"Error in auto-retrain check: {e}")
