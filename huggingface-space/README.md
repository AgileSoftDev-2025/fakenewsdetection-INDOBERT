---
title: IndoBERT Fake News Detection
emoji: 🔍
colorFrom: red
colorTo: orange
sdk: docker
pinned: false
license: mit
app_port: 7860
tags:
  - indonesian
  - fake-news
  - bert
  - classification
  - nlp
  - text-classification
models:
  - Davidbio/fakenewsdetection
---

# 🔍 IndoBERT Fake News Detection

Aplikasi deteksi berita hoax berbahasa Indonesia menggunakan model IndoBERT.

## 📖 Deskripsi

Model ini menggunakan **IndoBERT** (Indonesian BERT) yang telah di-fine-tune pada dataset berita Indonesia untuk mengklasifikasikan berita sebagai **Real** atau **Hoax (Fake News)**.

### ✨ Fitur

- 🤖 Deteksi otomatis berita hoax menggunakan deep learning
- 📊 Menampilkan confidence score dan probabilitas detail
- 🇮🇩 Dioptimalkan untuk teks berbahasa Indonesia
- ⚡ Interface yang mudah digunakan dengan Gradio

## 🚀 Cara Penggunaan

1. Masukkan teks berita pada kotak input
2. Klik tombol "🔍 Deteksi Berita"
3. Lihat hasil analisis:
   - Label prediksi (Real/Hoax)
   - Confidence score
   - Distribusi probabilitas

## 🎯 Model Information

- **Base Model:** indobenchmark/indobert-base-p1
- **Task:** Binary Text Classification
- **Classes:** 
  - 0: Real News
  - 1: Fake News (Hoax)
- **Max Sequence Length:** 256 tokens
- **Framework:** PyTorch + Transformers

## ⚠️ Disclaimer

Model ini adalah **alat bantu** dan tidak menjamin akurasi 100%. Selalu verifikasi informasi dari sumber terpercaya sebelum menyimpulkan sebuah berita sebagai hoax.

## 📚 Dataset

Model dilatih menggunakan dataset berita Indonesia yang telah dilabeli sebagai real atau hoax.

## 🛠️ Technology Stack

- **Framework:** Gradio
- **Model:** IndoBERT (Transformers)
- **Backend:** PyTorch
- **Deployment:** Hugging Face Spaces (Docker)

## 📝 Citation

Jika menggunakan model ini, mohon cantumkan:

```bibtex
@misc{indobert-fakenews,
  title={IndoBERT Fake News Detection},
  author={Your Name},
  year={2025},
  publisher={Hugging Face},
  howpublished={\url{https://huggingface.co/spaces/your-username/indobert-fakenews}}
}
```

## 📄 License

MIT License

---

**Developed with ❤️ for Indonesian NLP Community**
