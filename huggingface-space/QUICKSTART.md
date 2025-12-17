# 🚀 Hugging Face Space Setup - IndoBERT Fake News Detection

Setup lengkap untuk hosting model IndoBERT di Hugging Face Spaces.

## ✅ Status Setup

- ✅ Model sudah di-upload: [Davidbio/fakenewsdetection](https://huggingface.co/Davidbio/fakenewsdetection)
- ✅ Space siap deploy: [Davidbio/fakenewsdetection](https://huggingface.co/spaces/Davidbio/fakenewsdetection)
- ✅ Docker optimized (hanya file yang diperlukan)

## 📁 File yang Dibuat

```
huggingface-space/
├── 📄 app.py                    # ✅ Aplikasi Gradio (load dari HF Hub)
├── 🐳 Dockerfile                # ✅ Optimized untuk HF Spaces
├── 📦 requirements.txt          # ✅ Dependencies minimal
├── 📖 README.md                 # ✅ Space metadata + model link
├── 🚫 .gitignore               # ✅ Git ignore rules
├── 🚫 .dockerignore            # ✅ Exclude checkpoints & file tidak perlu
├── 📚 DEPLOY.md                # ✅ Panduan deploy spesifik
└── 🚀 deploy_to_space.ps1      # ✅ Auto-deploy script
```

## ⚡ Quick Deploy (3 Langkah)

### Cara 1: Script Otomatis (Termudah)

```powershell
cd huggingface-space
.\deploy_to_space.ps1
```

### Cara 2: Manual via Git

```powershell
# 1. Clone Space
git clone https://huggingface.co/spaces/Davidbio/fakenewsdetection
cd fakenewsdetection

# 2. Copy file yang diperlukan
Copy-Item ..\huggingface-space\app.py .
Copy-Item ..\huggingface-space\Dockerfile .
Copy-Item ..\huggingface-space\requirements.txt .
Copy-Item ..\huggingface-space\README.md .
Copy-Item ..\huggingface-space\.dockerignore .

# 3. Push
git add .
git commit -m "Deploy IndoBERT model"
git push
```

## 🎯 Fitur

✅ **Load dari HF Hub** - Model otomatis load dari HuggingFace Hub  
✅ **Docker optimized** - Hanya file yang diperlukan, tanpa checkpoint  
✅ **Interface Gradio** yang user-friendly  
✅ **Confidence scoring** dengan visualisasi  
✅ **Responsive UI** dengan theme modern  
✅ **Example texts** untuk demo  
✅ **Error handling** yang robust  

## 📊 Alur Kerja

1. User buka Space: https://huggingface.co/spaces/Davidbio/fakenewsdetection
2. Docker build (sudah optimized, cepat)
3. App load model dari: https://huggingface.co/Davidbio/fakenewsdetection
4. User input teks → Model prediksi → Hasil ditampilkan

## ⚙️ Yang Sudah Dikonfigurasi

- ✅ Model repo: `Davidbio/fakenewsdetection`
- ✅ `.dockerignore`: Exclude checkpoints & file tidak perlu
- ✅ `Dockerfile`: Load model dari HF Hub (tidak copy lokal)
- ✅ `app.py`: Prioritas load dari HF Hub
- ✅ `README.md`: Metadata dengan link ke model

## 🔍 File yang Di-Deploy ke Space

**HANYA 6 file ini:**
1. `app.py` - Aplikasi Gradio
2. `Dockerfile` - Docker configuration
3. `requirements.txt` - Python dependencies
4. `README.md` - Space metadata
5. `.dockerignore` - Exclude rules
6. `.gitignore` - Git rules

**TIDAK termasuk:**
- ❌ Folder `models/` (model di HF Hub)
- ❌ Training checkpoints
- ❌ Documentation files
- ❌ Test scripts
- ❌ Deploy scripts

## 📈 Monitoring

Space URL: https://huggingface.co/spaces/Davidbio/fakenewsdetection

Cek:
- **Build logs** - Status build Docker
- **App logs** - Model loading status
- **Analytics** - Usage statistics

## 💡 Tips

1. Model sudah di HF Hub, tidak perlu upload lagi
2. Space akan auto-rebuild setiap ada commit
3. Gunakan CPU tier dulu (gratis), upgrade ke GPU jika perlu
4. Monitor logs untuk troubleshooting

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Build failed | Cek build logs di Space page |
| Model not found | Verifikasi repo: Davidbio/fakenewsdetection |
| Slow loading | Upgrade hardware tier (CPU → GPU) |
| Out of memory | Gunakan T4 GPU tier |

---

**Space:** https://huggingface.co/spaces/Davidbio/fakenewsdetection  
**Model:** https://huggingface.co/Davidbio/fakenewsdetection

Lihat [DEPLOY.md](DEPLOY.md) untuk panduan lengkap!
