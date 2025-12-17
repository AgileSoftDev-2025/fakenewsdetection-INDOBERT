"""
Hugging Face Space Application - IndoBERT Fake News Detection
Menggunakan Gradio untuk interface yang user-friendly
"""

import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from pathlib import Path
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Konfigurasi - Model dari HuggingFace Hub
MODEL_REPO = "Davidbio/fakenewsdetection"  # Model yang sudah di-upload
MODEL_DIR = Path(__file__).parent / "models" / "indobert"  # Fallback lokal


class FakeNewsDetector:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_model()

    def load_model(self):
        """Load model dari HuggingFace Hub atau lokal"""
        try:
            # Load dari HuggingFace Hub (prioritas utama)
            hf_repo = os.environ.get("HF_MODEL_REPO", MODEL_REPO)
            logger.info(f"Loading model dari HuggingFace Hub: {hf_repo}")
            
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(hf_repo)
                self.model = AutoModelForSequenceClassification.from_pretrained(hf_repo)
                logger.info("✅ Model loaded dari HuggingFace Hub")
            except Exception as hub_error:
                # Fallback ke lokal jika HF Hub gagal
                if MODEL_DIR.exists() and any(MODEL_DIR.iterdir()):
                    logger.warning(f"HF Hub failed, loading from local: {hub_error}")
                    self.tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
                    self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
                    logger.info("✅ Model loaded dari lokal")
                else:
                    raise hub_error

            self.model.eval()
            self.model.to(self.device)
            logger.info(f"Model berhasil dimuat di {self.device}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def predict(self, text: str):
        """
        Prediksi apakah berita adalah hoax atau bukan
        Returns: (label, confidence, probabilities)
        """
        if not text or len(text.strip()) < 10:
            return (
                "Error",
                0.0,
                {"Real": 0.0, "Hoax": 0.0},
                "⚠️ Teks terlalu pendek. Minimal 10 karakter.",
            )

        try:
            # Tokenisasi
            encoded = self.tokenizer(
                text, truncation=True, max_length=256, return_tensors="pt"
            ).to(self.device)

            # Prediksi
            with torch.no_grad():
                logits = self.model(**encoded).logits
                probs = torch.softmax(logits, dim=-1).cpu().numpy()[0]

            # Ekstrak hasil
            prob_real = float(probs[0])
            prob_hoax = float(probs[1])
            predicted_label = int(np.argmax(probs))
            confidence = float(probs[predicted_label])

            # Label dan warning
            label_text = "🚨 HOAX" if predicted_label == 1 else "✅ REAL"

            # Confidence level
            if confidence >= 0.9:
                confidence_level = "Sangat Tinggi"
            elif confidence >= 0.75:
                confidence_level = "Tinggi"
            elif confidence >= 0.6:
                confidence_level = "Sedang"
            else:
                confidence_level = "Rendah"

            # Warning message
            warning = ""
            if confidence < 0.6:
                warning = "⚠️ Confidence rendah. Hasil mungkin tidak akurat. Silakan verifikasi secara manual."

            # Format hasil
            result_text = f"""
### Hasil Deteksi: {label_text}

**Confidence:** {confidence:.2%} ({confidence_level})

**Probabilitas Detail:**
- Real News: {prob_real:.2%}
- Fake News (Hoax): {prob_hoax:.2%}

{warning}
            """

            return (
                result_text,
                confidence,
                {"Real News": prob_real, "Fake News (Hoax)": prob_hoax},
                warning,
            )

        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return f"❌ Error: {str(e)}", 0.0, {"Real": 0.0, "Hoax": 0.0}, ""


# Inisialisasi detector
detector = FakeNewsDetector()


def predict_news(text: str):
    """Wrapper function untuk Gradio"""
    result_text, confidence, probs, warning = detector.predict(text)
    return result_text, probs


# Contoh teks untuk demo
examples = [
    [
        "Pemerintah mengumumkan kebijakan baru untuk meningkatkan ekonomi rakyat dengan subsidi langsung kepada UMKM."
    ],
    ["BREAKING: Alien mendarat di Jakarta dan bertemu dengan presiden!"],
    [
        "Menteri Kesehatan mengimbau masyarakat untuk tetap menjaga protokol kesehatan di tengah musim hujan."
    ],
]

# Buat Gradio Interface
with gr.Blocks(title="IndoBERT Fake News Detection", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🔍 IndoBERT Fake News Detection
    
    Deteksi berita hoax menggunakan model IndoBERT yang telah dilatih pada dataset berita Indonesia.
    
    **Cara Penggunaan:**
    1. Masukkan teks berita pada kotak di bawah
    2. Klik tombol "🔍 Deteksi Berita"
    3. Lihat hasil analisis dan tingkat confidence
    
    ⚠️ **Catatan:** Model ini adalah alat bantu dan tidak 100% akurat. Selalu verifikasi dari sumber terpercaya.
    """)

    with gr.Row():
        with gr.Column(scale=2):
            input_text = gr.Textbox(
                label="📝 Masukkan Teks Berita",
                placeholder="Ketik atau paste teks berita di sini...",
                lines=8,
                max_lines=15,
            )

            with gr.Row():
                clear_btn = gr.Button("🗑️ Clear", variant="secondary")
                submit_btn = gr.Button("🔍 Deteksi Berita", variant="primary")

        with gr.Column(scale=1):
            output_text = gr.Markdown(label="Hasil Deteksi")
            output_plot = gr.Label(label="Distribusi Probabilitas", num_top_classes=2)

    # Examples
    gr.Markdown("### 📋 Contoh Teks")
    gr.Examples(examples=examples, inputs=input_text, label="Klik untuk mencoba contoh")

    # Event handlers
    submit_btn.click(
        fn=predict_news, inputs=input_text, outputs=[output_text, output_plot]
    )

    clear_btn.click(
        fn=lambda: ("", "", {}),
        inputs=None,
        outputs=[input_text, output_text, output_plot],
    )

    gr.Markdown("""
    ---
    ### ℹ️ Tentang Model
    
    Model ini menggunakan **IndoBERT** (Indonesian BERT) yang telah di-fine-tune pada dataset berita Indonesia 
    untuk klasifikasi berita real vs hoax.
    
    - **Base Model:** indobenchmark/indobert-base-p1
    - **Task:** Binary Classification (Real/Hoax)
    - **Max Length:** 256 tokens
    
    ### 🤝 Kontribusi & Feedback
    
    Jika menemukan hasil yang kurang akurat, silakan laporkan untuk membantu meningkatkan model ini.
    """)

# Launch app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
