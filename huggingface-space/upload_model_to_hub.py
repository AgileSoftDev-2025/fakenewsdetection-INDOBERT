"""
Script untuk upload model IndoBERT ke Hugging Face Hub

Usage:
    python upload_model_to_hub.py --repo-name your-username/indobert-fakenews-model
"""

import argparse
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def upload_model(local_model_path: str, repo_name: str, private: bool = False):
    """Upload model ke Hugging Face Hub"""

    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        from huggingface_hub import HfApi, login
        import torch
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("Install dengan: pip install transformers huggingface-hub torch")
        sys.exit(1)

    # Verify local model exists
    model_path = Path(local_model_path)
    if not model_path.exists():
        print(f"❌ Error: Model tidak ditemukan di {model_path}")
        print(f"   Pastikan path benar: {model_path.absolute()}")
        sys.exit(1)

    print(f"📦 Loading model dari {model_path}")

    # Load model dan tokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        print("✅ Model berhasil dimuat")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        sys.exit(1)

    # Login ke HuggingFace
    print("\n🔐 Login ke Hugging Face...")
    print("Anda akan diminta untuk memasukkan HF token.")
    print("Dapatkan token di: https://huggingface.co/settings/tokens")

    try:
        login()
        print("✅ Login berhasil")
    except Exception as e:
        print(f"❌ Error login: {e}")
        sys.exit(1)

    # Upload model
    print(f"\n📤 Uploading model ke {repo_name}...")
    print("Ini mungkin memakan waktu beberapa menit...")

    try:
        # Upload tokenizer
        print("  Uploading tokenizer...")
        tokenizer.push_to_hub(
            repo_name,
            private=private,
            commit_message="Upload IndoBERT tokenizer for fake news detection",
        )

        # Upload model
        print("  Uploading model...")
        model.push_to_hub(
            repo_name,
            private=private,
            commit_message="Upload IndoBERT model for fake news detection",
        )

        print(f"\n✅ Upload berhasil!")
        print(f"🔗 Model tersedia di: https://huggingface.co/{repo_name}")

        # Create model card
        create_model_card(repo_name, private)

    except Exception as e:
        print(f"❌ Error uploading: {e}")
        sys.exit(1)


def create_model_card(repo_name: str, private: bool):
    """Create README.md untuk model card"""

    from huggingface_hub import HfApi

    model_card = f"""---
language: id
license: mit
tags:
  - indonesian
  - fake-news-detection
  - bert
  - text-classification
datasets:
  - custom
metrics:
  - accuracy
  - f1
---

# IndoBERT Fake News Detection Model

Model IndoBERT yang telah di-fine-tune untuk deteksi berita hoax berbahasa Indonesia.

## Model Description

Model ini adalah versi fine-tuned dari `indobenchmark/indobert-base-p1` untuk task klasifikasi binary (Real vs Hoax).

### Model Details

- **Model type:** BERT-based sequence classification
- **Language:** Indonesian (id)
- **Base model:** indobenchmark/indobert-base-p1
- **Task:** Binary Text Classification
- **Classes:** 
  - 0: Real News
  - 1: Fake News (Hoax)

## Intended Uses & Limitations

### Intended Uses

Model ini dirancang untuk:
- Deteksi awal berita hoax berbahasa Indonesia
- Screening otomatis konten berita
- Alat bantu fact-checking

### Limitations

⚠️ **PENTING:**
- Model ini **TIDAK** 100% akurat
- Harus digunakan sebagai **alat bantu**, bukan keputusan final
- Selalu verifikasi dari sumber terpercaya
- Performance bisa berbeda pada domain berita yang berbeda

## How to Use

### Basic Usage

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load model
model_name = "{repo_name}"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Predict
text = "Teks berita yang ingin dianalisis..."
inputs = tokenizer(text, truncation=True, max_length=256, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)
    prediction = torch.argmax(probs, dim=-1).item()

print(f"Prediction: {{'Real News' if prediction == 0 else 'Fake News'}}")
print(f"Confidence: {{probs[0][prediction].item():.2%}}")
```

### With Pipeline

```python
from transformers import pipeline

classifier = pipeline("text-classification", model="{repo_name}")
result = classifier("Teks berita yang ingin dianalisis...")
print(result)
```

## Training Data

Model dilatih menggunakan dataset berita Indonesia yang telah dilabeli sebagai real atau hoax.

## Training Procedure

### Training Hyperparameters

- Learning rate: (specify)
- Batch size: (specify)
- Epochs: (specify)
- Optimizer: AdamW
- Max sequence length: 256

## Evaluation Results

(Tambahkan metrics jika tersedia):
- Accuracy: XX%
- Precision: XX%
- Recall: XX%
- F1-Score: XX%

## Demo

Try the model on Hugging Face Spaces: [Link to Space]

## Citation

```bibtex
@misc{{indobert-fakenews-model,
  title={{IndoBERT Fake News Detection Model}},
  author={{Your Name}},
  year={{2025}},
  publisher={{Hugging Face}},
  url={{https://huggingface.co/{repo_name}}}
}}
```

## Contact

For questions or feedback, please open an issue in the [repository](link-to-your-repo).
"""

    try:
        api = HfApi()
        api.upload_file(
            path_or_fileobj=model_card.encode(),
            path_in_repo="README.md",
            repo_id=repo_name,
            repo_type="model",
            commit_message="Add model card",
        )
        print("📄 Model card created")
    except Exception as e:
        print(f"⚠️  Warning: Could not create model card: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Upload IndoBERT model to Hugging Face Hub"
    )
    parser.add_argument(
        "--local-model-path",
        type=str,
        default="../Model IndoBERT/models/indobert",
        help="Path ke model lokal (default: ../Model IndoBERT/models/indobert)",
    )
    parser.add_argument(
        "--repo-name",
        type=str,
        required=True,
        help="Nama repository di HF Hub (format: username/model-name)",
    )
    parser.add_argument(
        "--private", action="store_true", help="Buat repository private"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("🚀 IndoBERT Model Upload to Hugging Face Hub")
    print("=" * 60)
    print(f"Local model: {args.local_model_path}")
    print(f"Target repo: {args.repo_name}")
    print(f"Private: {args.private}")
    print("=" * 60)

    # Confirm
    confirm = input("\n⚠️  Lanjutkan upload? (y/n): ")
    if confirm.lower() != "y":
        print("Upload dibatalkan")
        sys.exit(0)

    upload_model(args.local_model_path, args.repo_name, args.private)

    print("\n" + "=" * 60)
    print("✅ SELESAI!")
    print("=" * 60)
    print("\nNext steps:")
    print(f"1. Verifikasi model di: https://huggingface.co/{args.repo_name}")
    print(f"2. Test model di Spaces dengan set environment variable:")
    print(f"   HF_MODEL_REPO={args.repo_name}")
    print("3. Update README.md dengan metrics dan info lengkap")


if __name__ == "__main__":
    main()
