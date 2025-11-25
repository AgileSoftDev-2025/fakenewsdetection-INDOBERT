from __future__ import annotations

from typing import Iterable, List, Tuple, Optional

from ..config import SETTINGS
from ..features import normalize_batch
from .. import feedback
from ..services.model_registry import get_current_version


def predict_fasttext(
    texts: Iterable[str],
    return_proba: bool = False,
    log_feedback: bool = False,
    user_labels: Optional[Iterable[Optional[int]]] = None,
) -> List[int] | Tuple[List[int], List[float]]:
    """Predict with FastText.

    If return_proba=True returns (preds, prob_hoax_list).
    If log_feedback=True also appends rows to feedback.csv.
    """
    import fasttext

    texts_list = list(texts)
    model = fasttext.load_model(SETTINGS.fasttext_model_path)
    norm = normalize_batch(texts_list)
    preds: List[int] = []
    probs_hoax: List[float] = []
    confidences: List[float] = []
    for t in norm:
        labels, scores = model.predict(t, k=2)
        # Map labels to probabilities (scores already softmax-like in fastText)
        lbl_map = {lab.replace("__label__", ""): sc for lab, sc in zip(labels, scores)}
        p1 = float(lbl_map.get("1", 0.0))
        # Determine predicted label as argmax
        pred = 1 if p1 >= 0.5 else 0
        conf = float(max(scores)) if scores else (p1 if p1 > 0 else 1 - p1)
        preds.append(pred)
        probs_hoax.append(p1)
        confidences.append(conf)

    if log_feedback:
        feedback.log_prediction(
            texts_list,
            preds,
            probs_hoax,
            confidences,
            model_name="fasttext",
            user_labels=user_labels,
        )

    if return_proba:
        return preds, probs_hoax
    return preds


def predict_indobert(
    texts: Iterable[str],
    return_proba: bool = False,
    log_feedback: bool = False,
    user_labels: Optional[Iterable[Optional[int]]] = None,
) -> List[int] | Tuple[List[int], List[float]]:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    import numpy as np

    texts_list = list(texts)
    tokenizer = AutoTokenizer.from_pretrained(SETTINGS.indobert_model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(
        SETTINGS.indobert_model_dir
    )
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    preds: List[int] = []
    probs_hoax: List[float] = []
    confidences: List[float] = []
    for t in texts_list:
        enc = tokenizer(t, truncation=True, max_length=256, return_tensors="pt").to(
            device
        )
        with torch.no_grad():
            logits = model(**enc).logits
            probs = torch.softmax(logits, dim=-1).cpu().numpy()[0]
            p1 = float(probs[1])  # probability for label=1
            pred = int(np.argmax(probs))
            conf = float(probs[pred])
        preds.append(pred)
        probs_hoax.append(p1)
        confidences.append(conf)

    if log_feedback:
        feedback.log_prediction(
            texts_list,
            preds,
            probs_hoax,
            confidences,
            model_name="indobert",
            model_version=get_current_version(),
            user_labels=user_labels,
        )

    if return_proba:
        return preds, probs_hoax
    return preds
