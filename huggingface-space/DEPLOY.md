# 🚀 Deploy Guide - Davidbio/fakenewsdetection

Panduan cepat untuk deploy ke HuggingFace Space Anda.

## ✅ Status

- ✅ Model sudah di-upload ke HF Hub: `Davidbio/fakenewsdetection`
- ✅ Setup sudah dikonfigurasi untuk Space: `https://huggingface.co/spaces/Davidbio/fakenewsdetection`

## 📦 File yang Perlu Di-Upload ke Space

Hanya upload file-file ini ke Space (sudah di-optimize):

```
huggingface-space/
├── app.py              # ✅ Aplikasi Gradio
├── Dockerfile          # ✅ Docker config (optimized)
├── requirements.txt    # ✅ Dependencies
├── README.md          # ✅ Metadata Space
├── .dockerignore      # ✅ Exclude file yang tidak perlu
└── .gitignore         # ✅ Git rules
```

**JANGAN upload:**
- ❌ Folder `models/` (model sudah di HF Hub)
- ❌ File `.md` lainnya (kecuali README.md)
- ❌ Scripts testing dan deployment
- ❌ Checkpoint training yang tidak terpakai

## 🚀 Cara Deploy

### Opsi 1: Via Git (Recommended)

```powershell
# 1. Clone Space repository
git clone https://huggingface.co/spaces/Davidbio/fakenewsdetection
cd fakenewsdetection

# 2. Copy HANYA file yang diperlukan
Copy-Item ..\huggingface-space\app.py .
Copy-Item ..\huggingface-space\Dockerfile .
Copy-Item ..\huggingface-space\requirements.txt .
Copy-Item ..\huggingface-space\README.md .
Copy-Item ..\huggingface-space\.dockerignore .
Copy-Item ..\huggingface-space\.gitignore .

# 3. Commit dan push
git add .
git commit -m "Deploy IndoBERT Fake News Detection"
git push
```

### Opsi 2: Via Web UI

1. Buka: https://huggingface.co/spaces/Davidbio/fakenewsdetection/tree/main
2. Upload file satu per satu:
   - `app.py`
   - `Dockerfile`
   - `requirements.txt`
   - `README.md`
   - `.dockerignore`
3. Tunggu build selesai

### Opsi 3: Via Script (Otomatis)

```powershell
cd huggingface-space
.\deploy_to_space.ps1
```

## ⚙️ Konfigurasi

Model akan otomatis load dari HF Hub dengan konfigurasi:

```
HF_MODEL_REPO = Davidbio/fakenewsdetection
```

Sudah di-set di `Dockerfile`, tidak perlu set manual di Space Settings.

## 🔍 Verifikasi

Setelah deploy:

1. ✅ Build berhasil (cek logs)
2. ✅ App running di: https://huggingface.co/spaces/Davidbio/fakenewsdetection
3. ✅ Model loading dari HF Hub (cek logs: "Loading model dari HuggingFace Hub")
4. ✅ Test prediksi dengan contoh teks

## 📊 Monitoring

Cek di Space page:
- **Build logs** - untuk debug jika ada error
- **App logs** - untuk monitor model loading
- **Analytics** - untuk usage statistics

## 🆘 Troubleshooting

### Build Failed
```
Cek: Build logs di Space page
Fix: Pastikan semua file sudah ter-upload
```

### Model Not Loading
```
Error: "Model not found"
Fix: Model repo sudah benar: Davidbio/fakenewsdetection
      Pastikan model di HF Hub accessible (public)
```

### Out of Memory
```
Fix: Upgrade Space hardware tier
     CPU → T4 GPU (Settings → Hardware)
```

## 🎯 Next Steps

Setelah deploy berhasil:

1. ✅ Test aplikasi dengan berbagai teks
2. ✅ Share link ke user
3. ✅ Monitor usage dan feedback
4. ✅ Update model jika perlu (re-run upload script)
5. ✅ Optimize berdasarkan analytics

---

**Space URL:** https://huggingface.co/spaces/Davidbio/fakenewsdetection  
**Model URL:** https://huggingface.co/Davidbio/fakenewsdetection
