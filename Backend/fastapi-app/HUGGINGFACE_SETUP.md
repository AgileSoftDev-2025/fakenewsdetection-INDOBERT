# Quick Start - Hugging Face Model Setup

Panduan cepat untuk mengatur backend agar menggunakan model dari Hugging Face Hub.

## 📋 Prerequisites

- Python 3.9+ installed
- Hugging Face account (free): https://huggingface.co/join
- Model uploaded to Hugging Face Hub

## 🚀 Setup Steps

### 1. Get Your Hugging Face Token

1. Login ke Hugging Face: https://huggingface.co/settings/tokens
2. Click **"New token"** atau gunakan token yang sudah ada
3. Select **"Read"** access (atau "Write" jika perlu upload)
4. Copy token (format: `hf_xxxxxxxxxxxxxxxxxxxxx`)

### 2. Configure Environment Variables

Dari folder `Backend/fastapi-app/`, copy file example:

```powershell
Copy-Item .env.example .env
```

Atau buat manual:

```powershell
New-Item .env -ItemType File
```

Edit file `.env` dan isi:

```env
HF_MODEL_REPO=Davidbio/fakenewsdetection-indobert
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx
```

**Ganti:**
- `Davidbio/fakenewsdetection-indobert` → Nama repo HF Anda
- `hf_xxxxxxxxxxxxxxxxxxxxx` → Token HF Anda yang sebenarnya

### 3. Test Connection

Sebelum start server, test dulu koneksi ke HF:

```powershell
# Ensure venv is activated
.venv\Scripts\Activate.ps1

# Run test script
python test_hf_connection.py
```

**Output yang diharapkan:**
```
==========================================================
HUGGING FACE CONFIGURATION TEST
==========================================================

1. Environment Variables:
   HF_MODEL_REPO: Davidbio/fakenewsdetection-indobert
   HF_TOKEN: ✓ SET (hidden)

2. Checking huggingface-hub installation...
   ✓ huggingface-hub is installed

3. Testing authentication...
   ✓ Authenticated as: YourUsername

4. Testing access to repository: Davidbio/fakenewsdetection-indobert
   ✓ Repository accessible
   ✓ Found 15 files in repository

   Required model files:
   ✓ config.json
   ✓ model.safetensors
   ✓ tokenizer.json
   ✓ vocab.txt

==========================================================
✓ ALL TESTS PASSED!
==========================================================
```

### 4. (Optional) Pindahkan Model Local

Jika Anda ingin backend HANYA menggunakan HF (tidak local), pindahkan folder model:

```powershell
# Backup model local
Move-Item "..\..\Model IndoBERT\models\indobert" "..\..\Model IndoBERT\models\indobert.backup"
```

### 5. Start Backend Server

```powershell
uvicorn app.main:app --reload --port 8000
```

**Saat startup pertama kali (tanpa model local):**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Downloading model snapshot from Davidbio/fakenewsdetection-indobert
INFO:     Model snapshot downloaded to C:\...\Model IndoBERT\models\indobert
INFO:     Application startup complete.
```

**Saat startup berikutnya:**
```
INFO:     Model directory exists locally, skipping download
INFO:     Application startup complete.
```

## 🔍 Troubleshooting

### Error: "HF_TOKEN not set"
- Pastikan file `.env` ada di folder `Backend/fastapi-app/`
- Cek isi file `.env`, pastikan `HF_TOKEN` tidak kosong
- Jangan ada spasi di sekitar `=`

### Error: "Authentication failed"
- Token mungkin salah atau expired
- Generate token baru di https://huggingface.co/settings/tokens
- Pastikan token dimulai dengan `hf_`

### Error: "Cannot access repository"
- Cek nama repository benar (`username/repo-name`)
- Jika repo private, pastikan token memiliki akses
- Verify di browser: https://huggingface.co/Davidbio/fakenewsdetection-indobert

### Download sangat lambat
- File model besar (~500MB+), butuh waktu 5-10 menit
- Pastikan koneksi internet stabil
- Download hanya terjadi sekali, subsequent starts cepat

### Error: "Model files not found"
- Cek folder `Model IndoBERT/models/indobert/` setelah download
- Jika kosong, coba delete folder dan restart server (akan re-download)
- Run `test_hf_connection.py` untuk verify file ada di HF repo

## 📝 Notes

**Model Loading Behavior:**
1. Backend check apakah model ada di local (`Model IndoBERT/models/indobert/`)
2. Jika ada → langsung pakai local (skip download)
3. Jika tidak ada DAN `HF_MODEL_REPO` di-set → download dari HF
4. Jika tidak ada DAN `HF_MODEL_REPO` TIDAK di-set → error saat predict

**Best Practice:**
- **Development:** Gunakan model local (lebih cepat)
- **Production/CI/CD:** Gunakan HF (auto-download di environment baru)
- **Team Collaboration:** Upload ke HF private repo, share token dengan team

## 🔗 Related Files

- `.env` - Configuration file (DO NOT COMMIT!)
- `.env.example` - Template untuk `.env`
- `test_hf_connection.py` - Test script untuk verify setup
- `app/main.py` - Contains `ensure_model_available()` startup hook

## 📚 Documentation

- Hugging Face Tokens: https://huggingface.co/docs/hub/security-tokens
- Model Hub: https://huggingface.co/docs/hub/models
- Python Hub API: https://huggingface.co/docs/huggingface_hub/
