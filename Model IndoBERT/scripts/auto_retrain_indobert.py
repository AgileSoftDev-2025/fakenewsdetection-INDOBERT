"""
Auto-retrain IndoBERT berdasarkan feedback berlabel.
Trigger: jumlah minimal feedback baru berlabel sejak retrain terakhir.

Pemakaian (jalankan dari root repo):
  # Pakai default threshold 50 baris
  python "Model IndoBERT\scripts\auto_retrain_indobert.py"

  # Atur threshold
  python "Model IndoBERT\scripts\auto_retrain_indobert.py" --threshold 100

Catatan:
- Feedback tanpa label (user_label kosong) akan diabaikan untuk retraining.
- Model versi baru akan diarsipkan ke folder models/indobert_versions, dan registry.json akan diperbarui.
- training set dibangun dari data awal + feedback berlabel, validasi & test tetap dari split awal atau bisa di-augment sesuai kebutuhan.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import List, Dict

import pandas as pd

# Ensure repo root on sys.path BEFORE project imports
here = Path(__file__).resolve()
repo_root = here.parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Project imports are done inside main() after sys.path is prepared


def load_feedback_since(last_id: int, feedback_path: str) -> List[Dict]:
    path = Path(feedback_path)
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                rid = int(r["id"])
            except Exception:
                continue
            if rid <= last_id:
                continue
            # hanya gunakan yang berlabel
            ul = r.get("user_label", "").strip()
            if ul == "":
                continue
            # normalisasi
            try:
                label = int(ul)
            except Exception:
                continue
            if label not in (0, 1):
                continue
            text = r.get("raw_text", "").replace("\\n", "\n")
            if not text.strip():
                continue
            rows.append({"id": rid, "text": text, "label": label})
    return rows


def main() -> None:
    # Late imports to avoid linter warning and ensure sys.path is set
    from src.feedback import FEEDBACK_FILE  # type: ignore
    from src.dataset import build_and_save_splits  # type: ignore
    from src.modeling.train import train_indobert, BertParams  # type: ignore
    from src.services.model_registry import (  # type: ignore
        get_last_used_feedback_id,
        set_last_used_feedback_id,
        next_version,
        archive_and_set_current,
    )

    parser = argparse.ArgumentParser(
        description="Auto-retrain IndoBERT dari feedback berlabel"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=50,
        help="Jumlah minimal feedback berlabel baru untuk memicu retrain",
    )
    parser.add_argument("--epochs", type=int, default=1, help="Epoch fine-tuning")
    parser.add_argument(
        "--batch-size", type=int, default=16, help="Batch size fine-tuning"
    )
    args = parser.parse_args()

    # Pastikan split dasar tersedia
    paths = build_and_save_splits()
    base_train = pd.read_csv(paths["train"])  # text,label,source
    base_val = pd.read_csv(paths["val"])  # text,label,source
    base_test = pd.read_csv(paths["test"])  # text,label,source

    last_id = get_last_used_feedback_id()
    new_rows = load_feedback_since(last_id, FEEDBACK_FILE)
    n_new = len(new_rows)
    if n_new < args.threshold:
        print(
            f"Belum retrain: feedback berlabel baru={n_new} < threshold={args.threshold}."
        )
        return

    print(f"Memicu retrain: ditemukan {n_new} feedback berlabel baru (ID>{last_id}).")
    fb_df = pd.DataFrame(new_rows)  # kolom: id, text, label

    # Bangun dataset training baru: base_train + feedback
    train_df = pd.concat(
        [base_train[["text", "label"]], fb_df[["text", "label"]]], ignore_index=True
    )
    # Validasi dan test tetap (opsi: tambahkan sebagian feedback untuk val jika ingin)
    val_df = base_val[["text", "label"]].copy()
    test_df = base_test[["text", "label"]].copy()

    # Fine-tune IndoBERT
    params = BertParams(epochs=args.epochs, batch_size=args.batch_size)
    metrics = train_indobert(
        train_df=train_df, val_df=val_df, test_df=test_df, params=params
    )

    # Naikkan versi dan arsipkan model
    ver = next_version()
    archive_path = archive_and_set_current(
        new_version=ver, metrics=metrics, feedback_rows_used=n_new
    )
    print(f"Model baru diarsipkan sebagai versi {ver}: {archive_path}")

    # Catat last used feedback id
    max_id = max(r["id"] for r in new_rows)
    set_last_used_feedback_id(max_id)
    print(f"Update last_used_feedback_id -> {max_id}")


if __name__ == "__main__":
    main()
