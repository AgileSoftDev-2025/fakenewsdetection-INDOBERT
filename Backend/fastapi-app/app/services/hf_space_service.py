"""
Service untuk integrasi dengan HuggingFace Space
Handles prediction requests to HF Space dengan fallback ke local model
"""

import httpx
import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# HF Space configuration
HF_SPACE_URL = os.getenv("HF_SPACE_URL", "https://davidbio-fakenewsdetection.hf.space")
HF_SPACE_API_KEY = os.getenv("HF_SPACE_API_KEY", "")  # Optional, jika Space private
ENABLE_HF_SPACE = os.getenv("ENABLE_HF_SPACE", "true").lower() == "true"
REQUEST_TIMEOUT = float(os.getenv("HF_SPACE_TIMEOUT", "30.0"))


class HFSpaceService:
    """Service untuk komunikasi dengan HuggingFace Space"""

    @staticmethod
    async def predict_via_space(text: str) -> Dict[str, Any]:
        """
        Kirim request prediksi ke HF Space API

        Args:
            text: Teks berita yang akan diprediksi

        Returns:
            Dictionary dengan hasil prediksi
        """
        try:
            logger.info(f"Sending prediction request to HF Space: {HF_SPACE_URL}")

            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                # Call FastAPI endpoint di HF Space
                response = await client.post(
                    f"{HF_SPACE_URL}/api/predict",
                    json={"text": text},
                    headers=(
                        {"Authorization": f"Bearer {HF_SPACE_API_KEY}"}
                        if HF_SPACE_API_KEY
                        else {}
                    ),
                )

                if response.status_code == 200:
                    result = response.json()
                    logger.info(
                        f"HF Space prediction success: {result.get('prediction')}"
                    )
                    return {
                        "success": True,
                        "prediction": result.get("prediction"),
                        "prob_hoax": result.get("prob_hoax"),
                        "confidence": result.get("confidence"),
                        "probabilities": result.get("probabilities", {}),
                        "model_version": result.get("model_version", "hf_space"),
                        "source": "hf_space",
                    }
                else:
                    logger.error(
                        f"HF Space API error: {response.status_code} - {response.text}"
                    )
                    return {
                        "success": False,
                        "error": f"API returned {response.status_code}: {response.text}",
                        "source": "hf_space",
                    }

        except httpx.TimeoutException:
            logger.error(f"HF Space API timeout after {REQUEST_TIMEOUT}s")
            return {
                "success": False,
                "error": f"Request timeout after {REQUEST_TIMEOUT}s",
                "source": "hf_space",
            }
        except Exception as e:
            logger.exception(f"Error calling HF Space API: {e}")
            return {"success": False, "error": str(e), "source": "hf_space"}

    @staticmethod
    async def predict_with_fallback(
        text: str, user_label: Optional[int] = None, log_feedback: bool = True
    ) -> Dict[str, Any]:
        """
        Prediksi dengan fallback ke local model jika HF Space gagal

        Args:
            text: Teks berita
            user_label: Label dari user (optional)
            log_feedback: Apakah feedback di-log untuk retrain

        Returns:
            Dictionary hasil prediksi
        """
        # Try HF Space first (jika enabled)
        if ENABLE_HF_SPACE:
            result = await HFSpaceService.predict_via_space(text)

            if result["success"]:
                # Log feedback ke local CSV dan PostgreSQL database
                if log_feedback:
                    try:
                        # 1. Log ke CSV untuk retrain (Railway: use stub)
                        try:
                            from src.modeling.predict import (
                                predict_indobert,
                            )  # type: ignore
                        except ModuleNotFoundError:
                            from .predict_stub import predict_indobert

                        predict_indobert(
                            [text],
                            return_proba=False,
                            log_feedback=True,
                            user_labels=[user_label]
                            if user_label is not None
                            else None,
                        )
                        logger.debug("Feedback logged to CSV for future retrain")
                    except Exception as e:
                        logger.warning(f"Failed to log feedback to CSV: {e}")

                    # 2. Log ke PostgreSQL database
                    try:
                        from ..database import get_db
                        from ..models import Feedback
                        import time

                        db = next(get_db())
                        feedback_entry = Feedback(
                            timestamp=int(time.time()),  # Epoch timestamp as integer
                            model_name="indobert",
                            model_version=result.get("model_version", "hf_space"),
                            text_length=len(text),
                            prediction=int(result["prediction"]),
                            prob_hoax=float(result["prob_hoax"]),
                            confidence=float(
                                result.get("confidence", result["prob_hoax"])
                            ),
                            user_label=user_label,
                            agreement="unknown"
                            if user_label is None
                            else (
                                "yes" if user_label == result["prediction"] else "no"
                            ),
                            raw_text=text,
                        )
                        db.add(feedback_entry)
                        db.commit()
                        logger.debug(
                            f"Feedback logged to PostgreSQL (id={feedback_entry.id})"
                        )
                    except Exception as e:
                        logger.warning(f"Failed to log feedback to PostgreSQL: {e}")

                return result

            # Log fallback
            logger.warning(
                f"HF Space prediction failed: {result.get('error')}, falling back to local model"
            )

        # Fallback to local model
        return await HFSpaceService.predict_local(text, user_label, log_feedback)

    @staticmethod
    async def predict_local(
        text: str, user_label: Optional[int] = None, log_feedback: bool = True
    ) -> Dict[str, Any]:
        """
        Prediksi menggunakan model local

        Args:
            text: Teks berita
            user_label: Label dari user
            log_feedback: Apakah log feedback

        Returns:
            Dictionary hasil prediksi
        """
        try:
            # Use stub in Railway production
            try:
                from src.modeling.predict import predict_indobert  # type: ignore
                from src.services.model_registry import get_current_version  # type: ignore
            except ModuleNotFoundError:
                from .predict_stub import predict_indobert
                from .model_registry_stub import get_current_version

            logger.info("Using local model for prediction")

            preds, probs = predict_indobert(
                [text],
                return_proba=True,
                log_feedback=log_feedback,  # This logs to CSV
                user_labels=[user_label] if user_label is not None else None,
            )  # type: ignore

            prediction = int(preds[0])
            prob_hoax = float(probs[0])
            confidence = prob_hoax if prediction == 1 else (1 - prob_hoax)

            # Also log to PostgreSQL database
            if log_feedback:
                try:
                    from ..database import get_db
                    from ..models import Feedback
                    import time

                    db = next(get_db())
                    feedback_entry = Feedback(
                        timestamp=int(time.time()),  # Epoch timestamp as integer
                        model_name="indobert",
                        model_version=get_current_version(),
                        text_length=len(text),
                        prediction=prediction,
                        prob_hoax=prob_hoax,
                        confidence=confidence,
                        user_label=user_label,
                        agreement="unknown"
                        if user_label is None
                        else ("yes" if user_label == prediction else "no"),
                        raw_text=text,
                    )
                    db.add(feedback_entry)
                    db.commit()
                    logger.debug(
                        f"Feedback logged to PostgreSQL (id={feedback_entry.id})"
                    )
                except Exception as e:
                    logger.warning(f"Failed to log feedback to PostgreSQL: {e}")

            return {
                "success": True,
                "prediction": prediction,
                "prob_hoax": prob_hoax,
                "confidence": confidence,
                "model_version": get_current_version(),
                "source": "local_model",
            }

        except Exception as e:
            logger.exception(f"Local model prediction error: {e}")
            return {
                "success": False,
                "error": f"Local model error: {str(e)}",
                "source": "local_model",
            }

    @staticmethod
    def check_space_health() -> Dict[str, Any]:
        """
        Check health status dari HF Space

        Returns:
            Dictionary dengan status health
        """
        try:
            import httpx

            response = httpx.get(f"{HF_SPACE_URL}/api/health", timeout=10.0)

            if response.status_code == 200:
                return {
                    "healthy": True,
                    "url": HF_SPACE_URL,
                    "response": response.json(),
                }
            else:
                return {
                    "healthy": False,
                    "url": HF_SPACE_URL,
                    "error": f"Status {response.status_code}",
                }

        except Exception as e:
            return {"healthy": False, "url": HF_SPACE_URL, "error": str(e)}
