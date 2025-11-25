# Backend - Fake News Detection API

Framework used: **FastAPI**

This backend provides REST API endpoints for Indonesian fake news detection using IndoBERT model, with support for text input, OCR from images, and DOCX document parsing.

## 📁 Project Structure

```
Backend/fastapi-app/
├── app/
│   ├── main.py              # FastAPI app with startup hooks
│   ├── api/
│   │   ├── predict.py       # Prediction endpoints (text & file)
│   │   └── feedback.py      # Feedback management
│   └── ...
├── requirements.txt         # Python dependencies
└── README.md
```

## 🚀 Setup Instructions (Windows)

### 1. Create and activate virtual environment

```powershell
cd Backend/fastapi-app
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

**Note:** This will install all required dependencies including:
- FastAPI & Uvicorn (web framework & ASGI server)
- PyTorch & Transformers (ML model)
- Tesseract OCR & python-docx (document processing)
- Hugging Face Hub (model downloading)

### 3. Configure Environment Variables

**Option A: Use Hugging Face Model (Recommended for Production)**

Copy the example .env file and configure your Hugging Face credentials:

```powershell
Copy-Item .env.example .env
# Edit .env and add your HF token
```

Edit `.env` file:
```env
HF_MODEL_REPO=Davidbio/fakenewsdetection-indobert
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx
```

**Get your Hugging Face token:**
1. Visit https://huggingface.co/settings/tokens
2. Login to your account
3. Create a new token (or use existing one)
4. Copy the token and paste it in `.env` file

**Test your configuration:**
```powershell
python test_hf_connection.py
```

This will verify:
- ✓ Environment variables are set
- ✓ Hugging Face authentication works
- ✓ Model repository is accessible
- ✓ Required model files exist

**Option B: Use Local Model (For Development)**

If you have model files locally at `Model IndoBERT/models/indobert/`, you can skip the Hugging Face setup. The backend will automatically use local files if available.

**Model Loading Priority:**
1. Check if model exists locally → Use local files
2. If HF_MODEL_REPO is set AND model not local → Download from HF
3. On subsequent starts → Always use local (no re-download)

### 4. Install Tesseract OCR (for image processing)

Download and install Tesseract OCR:
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Add to PATH or set `TESSERACT_CMD` environment variable

### 5. Run the server

```powershell
uvicorn app.main:app --reload --port 8000
```

Server will start on: **http://localhost:8000**

## 📡 API Endpoints

### Health Check
```http
GET /health
Response: { "status": "ok" }
```

### Predict from Text
```http
POST /predict
Content-Type: application/json

Body:
{
  "title": "Optional title",
  "text": "News text content",
  "body": "News body content",
  "log_feedback": true,
  "user_label": 0
}

Response:
{
  "prediction": 0,          # 0 = Valid, 1 = Hoax
  "prob_hoax": 0.1234,
  "model_version": "indobert-base"
}
```

### Predict from File (Image OCR or DOCX)
```http
POST /predict-file
Content-Type: multipart/form-data

Body:
- file: [PNG/JPG/DOCX file]
- log_feedback: "true"

Response:
{
  "prediction": 0,
  "prob_hoax": 0.1234,
  "model_version": "indobert-base",
  "extracted_text": "Text extracted from file..."
}
```

**Supported formats:**
- Images: PNG, JPG (via Tesseract OCR with Indonesian + English)
- Documents: DOCX (text extraction via python-docx)

### Feedback Management
```http
GET /feedback?limit=50
Response: [{ id, timestamp, prediction, user_label, ... }]

PATCH /feedback/{id}
Body: { "user_label": 0 }
Response: { "message": "Feedback updated" }
```

### Model Version
```http
GET /model/version
Response: { "version": "indobert-base", "path": "..." }
```

## 🗂️ Model Integration

The API imports and reuses code from `Model IndoBERT/src` module. Model files should exist at:
- `Model IndoBERT/models/indobert/` (local)
- Or auto-downloaded from Hugging Face Hub on startup

## 💾 Data Storage

Feedback is stored at: `Model IndoBERT/data/feedback/feedback.csv`

## 🧪 Testing

Run backend tests:
```powershell
pytest tests/
```

## 🔧 Troubleshooting

**Issue: uvicorn not found**
```powershell
pip install --force-reinstall uvicorn[standard]
```

**Issue: PyTorch DLL error on Windows**
```powershell
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**Issue: Tesseract not found**
- Ensure Tesseract is installed and in PATH
- Or set: `$env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"`

**Issue: Model not found**
- Ensure model files exist in `Model IndoBERT/models/indobert/`
- Or configure HF_MODEL_REPO and HF_TOKEN for auto-download

## 📦 Dependencies Overview

| Library | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.115.0 | Web framework |
| uvicorn | 0.30.6 | ASGI server |
| torch | ≥2.0.0 | Deep learning |
| transformers | ≥4.30.0 | IndoBERT model |
| pytesseract | 0.3.13 | OCR processing |
| python-docx | 1.1.2 | DOCX parsing |
| huggingface-hub | ≥0.18.1 | Model download |

## 🔗 Related

- Frontend: `Frontend/nextjs-app/`
- Model Training: `Model IndoBERT/`
- BDD Tests: `tests/bdd/`
