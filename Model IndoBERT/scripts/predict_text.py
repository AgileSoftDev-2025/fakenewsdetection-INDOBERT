"""
Simple CLI to run FastText and/or IndoBERT predictions on a given text.

Usage examples (run from repo root):
  python scripts/predict_text.py --title "Judul" --body "Isi ..." --model both
  python scripts/predict_text.py --text "Kalimat lengkap ..." --model indobert
  python scripts/predict_text.py --text-file path/to/file.txt --model fasttext

Note: This script ensures the repo root is on sys.path so that `src` can be imported
without needing to install the package.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _ensure_repo_on_syspath() -> None:
    # Add repo root (parent of this scripts folder) to sys.path if needed
    here = Path(__file__).resolve()
    repo_root = here.parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


_ensure_repo_on_syspath()

# Now we can import project functions
try:
    from src.modeling.predict import predict_fasttext, predict_indobert
    from src.feedback import FEEDBACK_FILE
except Exception:
    print("Gagal mengimpor modul prediksi dari src. Pastikan menjalankan dari root repo.")
    raise


def build_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.text_file:
        path = Path(args.text_file)
        return path.read_text(encoding="utf-8")
    if args.title or args.body:
        title = (args.title or "").strip()
        body = (args.body or "").strip()
        return f"{title}\n\n{body}".strip()
    raise SystemExit("Harap isi salah satu: --text, --text-file, atau gabungan --title/--body")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prediksi hoaks/bukan hoaks dengan FastText/IndoBERT (+opsional logging feedback)")
    parser.add_argument("--title", type=str, default=None, help="Judul teks (opsional)")
    parser.add_argument("--body", type=str, default=None, help="Isi teks (opsional)")
    parser.add_argument("--text", type=str, default=None, help="Teks lengkap (alternatif)")
    parser.add_argument("--text-file", type=str, default=None, help="File berisi teks (alternatif)")
    parser.add_argument(
        "--model",
        type=str,
        choices=["fasttext", "indobert", "both"],
        default="both",
        help="Model yang digunakan",
    )
    parser.add_argument("--log", action="store_true", help="Aktifkan logging ke feedback.csv")
    parser.add_argument("--user-label", type=int, choices=[0, 1], default=None, help="Label user (0=bukan hoaks,1=hoaks) untuk semua teks (opsional)")
    parser.add_argument("--return-proba", action="store_true", help="Tampilkan probabilitas hoaks (label=1)")

    args = parser.parse_args()
    text = build_text(args)

    def label_to_str(y: int) -> str:
        return "hoaks" if int(y) == 1 else "bukan hoaks"

    if args.model in ("fasttext", "both"):
        if args.return_proba:
            (y_ft_list, p_ft_list) = predict_fasttext(
                [text], return_proba=True, log_feedback=args.log, user_labels=[args.user_label]
            )  # type: ignore
            y_ft = y_ft_list[0]
            p_ft = p_ft_list[0]
            print(f"FastText: {label_to_str(y_ft)} (p_hoax={p_ft:.4f})")
        else:
            y_ft = predict_fasttext([text], log_feedback=args.log, user_labels=[args.user_label])[0]
            print(f"FastText: {label_to_str(y_ft)}")

    if args.model in ("indobert", "both"):
        if args.return_proba:
            (y_bert_list, p_bert_list) = predict_indobert(
                [text], return_proba=True, log_feedback=args.log, user_labels=[args.user_label]
            )  # type: ignore
            y_bert = y_bert_list[0]
            p_bert = p_bert_list[0]
            print(f"IndoBERT: {label_to_str(y_bert)} (p_hoax={p_bert:.4f})")
        else:
            y_bert = predict_indobert([text], log_feedback=args.log, user_labels=[args.user_label])[0]
            print(f"IndoBERT: {label_to_str(y_bert)}")

    if args.log:
        print(f"Feedback tersimpan di: {FEEDBACK_FILE}")


if __name__ == "__main__":
    main()
