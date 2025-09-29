"""
Tampilkan N baris terakhir dari feedback.csv agar mudah melihat ID yang baru ditambahkan.

Contoh:
  python "Model IndoBERT\scripts\tail_feedback.py" --n 10
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def _ensure_repo_on_syspath() -> None:
    here = Path(__file__).resolve()
    repo_root = here.parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


_ensure_repo_on_syspath()

try:
    from src.feedback import FEEDBACK_FILE
except Exception:
    print(
        "Gagal mengimpor modul feedback dari src. Pastikan menjalankan dari root repo."
    )
    raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tampilkan N baris terakhir dari feedback.csv"
    )
    parser.add_argument(
        "--n", type=int, default=5, help="Jumlah baris terakhir yang ditampilkan"
    )
    args = parser.parse_args()

    path = Path(FEEDBACK_FILE)
    if not path.exists():
        print(f"File feedback belum ada: {path}")
        return

    # Baca seluruh isi (file relatif kecil), alternatif: streaming jika besar
    rows = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    tail_rows = rows[-args.n :] if args.n > 0 else rows
    if not tail_rows:
        print("Tidak ada data.")
        return

    # Cetak ringkas kolom utama
    print(f"Menampilkan {len(tail_rows)} baris terakhir dari {path}:")
    for r in tail_rows:
        print(
            f"id={r['id']} | ts={r['timestamp']} | model={r['model_name']} | pred={r['prediction']} | p1={r['prob_hoax']} | user_label={r['user_label']} | agreement={r['agreement']} | len={r['text_length']}"
        )


if __name__ == "__main__":
    main()
