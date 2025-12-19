"""
Stub untuk src.modeling.predict - digunakan di Railway production

Di Railway, backend hanya melakukan API call ke HF Space untuk inference.
File ini menyediakan stub functions untuk menghindari ModuleNotFoundError.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def predict_indobert(text, user_label: Optional[int] = None, **kwargs) -> Dict[str, Any]:
    """
    Stub untuk local model prediction.
    
    Di Railway production, ini hanya untuk logging feedback, bukan untuk actual prediction.
    Function ini akan gracefully return empty result karena prediction sudah dilakukan
    via HF Space API.
    
    Args:
        text: Text berita untuk diprediksi (bisa list atau string)
        user_label: Optional user feedback label (0 atau 1)
        **kwargs: Additional arguments (log_feedback, return_proba, etc.)
        
    Returns:
        Empty tuple for Railway (actual prediction comes from HF Space)
    """
    logger.info("predict_indobert() called in Railway - used only for feedback logging")
    
    # Di Railway, function ini dipanggil hanya untuk log feedback
    # Actual prediction sudah dilakukan oleh HF Space API
    # Jadi kita hanya return empty result
    
    return_proba = kwargs.get("return_proba", False)
    
    if return_proba:
        # Return (predictions, probabilities) tuple
        return ([], [])
    else:
        # Return predictions only
        return []


def load_indobert_model():
    """Stub untuk model loading - not needed in Railway"""
    logger.warning("load_indobert_model() called in Railway - this should not happen!")
    raise RuntimeError("Model loading not available in Railway production")


def get_model_info() -> Dict[str, Any]:
    """Get model info stub"""
    logger.info("Using stub get_model_info() - Railway production mode")
    return {
        "model_name": "IndoBERT (via HF Space)",
        "source": "huggingface_space",
        "local_model_loaded": False,
    }
