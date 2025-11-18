from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

# Path tempat menyimpan model
model_path = r"C:\Users\ASUS\fakenewsdetection-INDOBERT\Model IndoBERT\models\indobert"

# Buat folder jika belum ada
os.makedirs(model_path, exist_ok=True)

print("Downloading model...")

# Download model IndoBERT dari Hugging Face
model = AutoModelForSequenceClassification.from_pretrained(
    "indobenchmark/indobert-base-p1",
    num_labels=2
)
tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p1")

# Simpan model
print("Saving model...")
model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)

print(f"Model berhasil disimpan di: {model_path}")