from __future__ import annotations

from typing import Optional
from io import BytesIO
import os
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

# Import project functions
from src.modeling.predict import predict_indobert  # type: ignore
from src.services.model_registry import get_current_version  # type: ignore

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
async def predict(req: PredictRequest) -> PredictResponse:
    # Build text from fields
    text = (req.text or "").strip()
    if not text:
        title = (req.title or "").strip()
        body = (req.body or "").strip()
        text = (title + "\n\n" + body).strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text/title/body is required")

    try:
        preds, probs = predict_indobert(
            [text],
            return_proba=True,
            log_feedback=req.log_feedback,
            user_labels=[req.user_label],
        )  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")

    model_version = get_current_version()
    return PredictResponse(
        prediction=int(preds[0]), prob_hoax=float(probs[0]), model_version=model_version
    )


@router.post("/predict-file", response_model=PredictFileResponse)
async def predict_file(
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

    try:
        preds, probs = predict_indobert(
            [text],
            return_proba=True,
            log_feedback=log_feedback,
            user_labels=[user_label],
        )  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")

    model_version = get_current_version()
    return PredictFileResponse(
        prediction=int(preds[0]),
        prob_hoax=float(probs[0]),
        model_version=model_version,
        extracted_text=text,
    )
