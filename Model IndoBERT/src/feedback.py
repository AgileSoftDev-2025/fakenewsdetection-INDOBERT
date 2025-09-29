from __future__ import annotations

import csv
import os
import time
from typing import Iterable, List, Optional

from .config import SETTINGS


FEEDBACK_FILE = os.path.join(SETTINGS.feedback_dir, "feedback.csv")

FIELDNAMES = [
    "id",  # unique incremental id
    "timestamp",  # epoch seconds
    "model_name",  # fasttext | indobert
    "model_version",  # placeholder (could be commit hash / date)
    "text_length",
    "prediction",  # int
    "prob_hoax",  # probability of class=1
    "confidence",  # max probability across classes
    "user_label",  # int or blank
    "agreement",  # user_label == prediction (yes/no/unknown)
    "raw_text",  # original text (could be truncated externally if needed)
]


def _init_file() -> None:
    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, FIELDNAMES)
            writer.writeheader()


def _next_id() -> int:
    if not os.path.exists(FEEDBACK_FILE):
        return 1
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            # read last non-empty line to get id (avoid loading full file in memory)
            last_line = None
            for line in f:
                if line.strip():
                    last_line = line
            if last_line:
                parts = last_line.split(",", 1)
                return int(parts[0]) + 1
    except Exception:
        return 1
    return 1


def log_prediction(
    texts: Iterable[str],
    predictions: Iterable[int],
    probs_hoax: Iterable[float],
    confidences: Iterable[float],
    model_name: str,
    model_version: str = "v1",
    user_labels: Optional[Iterable[Optional[int]]] = None,
) -> List[int]:
    """Append prediction rows to feedback.csv

    Returns list of assigned row ids.
    """
    _init_file()
    ids: List[int] = []
    if user_labels is None:
        user_labels = [None] * len(list(predictions))  # type: ignore

    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, FIELDNAMES)
        for text, pred, p1, conf, ul in zip(
            texts, predictions, probs_hoax, confidences, user_labels
        ):
            rid = _next_id()
            agreement = "unknown"
            if ul is not None:
                agreement = "yes" if int(ul) == int(pred) else "no"
            writer.writerow(
                {
                    "id": rid,
                    "timestamp": int(time.time()),
                    "model_name": model_name,
                    "model_version": model_version,
                    "text_length": len(text),
                    "prediction": int(pred),
                    "prob_hoax": float(p1),
                    "confidence": float(conf),
                    "user_label": "" if ul is None else int(ul),
                    "agreement": agreement,
                    "raw_text": text.replace("\n", "\\n"),
                }
            )
            ids.append(rid)
    return ids


def update_user_label(row_id: int, user_label: int) -> bool:
    """Update user_label & agreement for a given row id.
    Returns True if updated, False if row not found.
    """
    if not os.path.exists(FEEDBACK_FILE):
        return False
    rows = []
    updated = False
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if int(r["id"]) == row_id:
                r["user_label"] = int(user_label)
                agreement = "yes" if int(r["prediction"]) == int(user_label) else "no"
                r["agreement"] = agreement
                updated = True
            rows.append(r)
    if updated:
        with open(FEEDBACK_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, FIELDNAMES)
            writer.writeheader()
            writer.writerows(rows)
    return updated


def iter_feedback(limit: Optional[int] = None):
    if not os.path.exists(FEEDBACK_FILE):
        return []
    out = []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, r in enumerate(reader):
            if limit is not None and i >= limit:
                break
            out.append(r)
    return out


__all__ = [
    "log_prediction",
    "update_user_label",
    "iter_feedback",
    "FEEDBACK_FILE",
]
