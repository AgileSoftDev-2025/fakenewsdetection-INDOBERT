"""
Stub untuk src.feedback - digunakan di Railway production

Di Railway, feedback storage masih berfungsi tapi tidak trigger retrain otomatis.
File ini menyediakan stub functions untuk menghindari ModuleNotFoundError.
"""

import logging
from typing import Optional, Iterator, Dict, Any
from pathlib import Path
import json
import os

logger = logging.getLogger(__name__)

# Use /tmp for feedback in Railway (ephemeral, tapi cukup untuk logging)
FEEDBACK_DIR = Path(os.getenv("FEEDBACK_DIR", "/tmp/feedback"))
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)


def update_user_label(
    text: str,
    prediction: int,
    user_label: int,
    prob_hoax: float = 0.0,
    metadata: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Save user feedback for future retraining.
    
    Di Railway, ini akan save ke /tmp (ephemeral storage).
    Di production, feedback sebaiknya disimpan ke database atau S3.
    
    Args:
        text: Text yang diprediksi
        prediction: Model prediction (0 atau 1)
        user_label: User's actual label (0 atau 1)
        prob_hoax: Probability of hoax from model
        metadata: Optional additional metadata
        
    Returns:
        True if feedback saved successfully
    """
    try:
        feedback_file = FEEDBACK_DIR / "feedback.jsonl"
        
        feedback_entry = {
            "text": text,
            "prediction": prediction,
            "user_label": user_label,
            "prob_hoax": prob_hoax,
            "metadata": metadata or {},
        }
        
        # Append to JSONL file
        with open(feedback_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(feedback_entry, ensure_ascii=False) + "\n")
        
        logger.info(f"Feedback saved to {feedback_file}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save feedback: {e}")
        return False


def iter_feedback(
    limit: Optional[int] = None, only_unlabeled: bool = False
) -> Iterator[Dict[str, Any]]:
    """
    Iterate through feedback entries.
    
    Args:
        limit: Maximum number of entries to return
        only_unlabeled: If True, only return entries without user_label
        
    Yields:
        Feedback dictionaries
    """
    try:
        feedback_file = FEEDBACK_DIR / "feedback.jsonl"
        
        if not feedback_file.exists():
            logger.warning(f"Feedback file not found: {feedback_file}")
            return
        
        count = 0
        with open(feedback_file, "r", encoding="utf-8") as f:
            for line in f:
                if limit and count >= limit:
                    break
                    
                try:
                    entry = json.loads(line.strip())
                    
                    if only_unlabeled and entry.get("user_label") is not None:
                        continue
                    
                    yield entry
                    count += 1
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON in feedback file: {e}")
                    continue
                    
    except Exception as e:
        logger.error(f"Error reading feedback: {e}")


def get_feedback_count() -> int:
    """Get total number of feedback entries"""
    try:
        feedback_file = FEEDBACK_DIR / "feedback.jsonl"
        
        if not feedback_file.exists():
            return 0
        
        with open(feedback_file, "r") as f:
            return sum(1 for _ in f)
            
    except Exception as e:
        logger.error(f"Error counting feedback: {e}")
        return 0
