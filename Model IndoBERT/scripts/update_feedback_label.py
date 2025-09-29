r"""
CLI kecil untuk memperbarui user_label pada feedback.csv berdasarkan ID baris.

Contoh pemakaian (jalankan dari root repo):
    python "Model IndoBERT\scripts\update_feedback_label.py" --id 123 --user-label 1

Keterangan label:
    0 = bukan hoaks
    1 = hoaks
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _ensure_repo_on_syspath() -> None:
    here = Path(__file__).resolve()
    repo_root = here.parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


_ensure_repo_on_syspath()

try:
    from src.feedback import update_user_label, FEEDBACK_FILE
except Exception:
    print(
        "Gagal mengimpor modul feedback dari src. Pastikan menjalankan dari root repo."
    )
    raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Perbarui user_label di feedback.csv berdasarkan ID."
    )
    parser.add_argument(
        "--id", type=int, required=True, help="ID baris pada feedback.csv"
    )
    parser.add_argument(
        "--user-label",
        type=int,
        choices=[0, 1],
        required=True,
        help="Label user: 0=bukan hoaks, 1=hoaks",
    )
    args = parser.parse_args()

    ok = update_user_label(args.id, args.user_label)
    if ok:
        print(
            f"Berhasil memperbarui row id={args.id} menjadi user_label={args.user_label}."
        )
        print(f"File: {FEEDBACK_FILE}")
    else:
        print(
            f"Gagal memperbarui: ID {args.id} tidak ditemukan atau file feedback belum ada."
        )
        print(f"File: {FEEDBACK_FILE}")


if __name__ == "__main__":
    main()
