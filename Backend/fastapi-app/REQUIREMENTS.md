# Backend Requirements & Dependencies

## 📦 Python Dependencies

All dependencies are managed via `requirements.txt` and installed with `pip install -r requirements.txt`.

## Core Dependencies

### Web Framework

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **fastapi** | 0.115.0 | Modern async web framework for APIs | [FastAPI Docs](https://fastapi.tiangolo.com) |
| **uvicorn[standard]** | 0.30.6 | ASGI server with hot reload & WebSocket | [Uvicorn Docs](https://www.uvicorn.org) |
| **pydantic** | 2.9.2 | Data validation using Python type hints | [Pydantic Docs](https://docs.pydantic.dev) |

### File Processing

| Package | Version | Purpose |
|---------|---------|---------|
| **python-multipart** | 0.0.17 | File upload support for FastAPI |
| **pytesseract** | 0.3.13 | Python wrapper for Tesseract OCR |
| **python-docx** | 1.1.2 | Read/write DOCX files |
| **Pillow** | ≥8.0.0 | Image processing library |

### Machine Learning

| Package | Version | Purpose |
|---------|---------|---------|
| **torch** | ≥2.0.0 | PyTorch deep learning framework |
| **transformers** | ≥4.30.0 | Hugging Face transformers (IndoBERT) |
| **huggingface-hub** | ≥0.18.1 | Download models from Hugging Face |

### Data Processing

| Package | Version | Purpose |
|---------|---------|---------|
| **pandas** | ≥2.0.0 | Data manipulation and analysis |
| **numpy** | ≥1.24.0 | Numerical computing |
| **scikit-learn** | ≥1.3.0 | Machine learning utilities |

### Utilities

| Package | Version | Purpose |
|---------|---------|---------|
| **python-dotenv** | ≥1.0.0 | Load environment variables from .env file |

## 🛠️ System Requirements

### Minimum Requirements
- **Python:** 3.9 or higher (3.11 recommended)
- **pip:** 21.0 or higher
- **OS:** Windows 10/11, macOS, Linux
- **RAM:** 4GB minimum, 8GB recommended (for model loading)
- **Disk Space:** 
  - 2GB for dependencies
  - 1GB for model files
  - Total: ~3GB

### External Dependencies
- **Tesseract OCR:** Required for image text extraction
  - Windows: [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)
  - Add to PATH or set `TESSERACT_CMD` environment variable

## 📋 Installation Steps

### 1. Check Python Version
```powershell
python --version  # Should be 3.9+
pip --version     # Should be 21.0+
```

### 2. Create Virtual Environment
```powershell
cd Backend/fastapi-app
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Why virtual environment?**
- Isolates project dependencies
- Prevents conflicts with system packages
- Easy to recreate/reset

### 3. Upgrade pip
```powershell
python -m pip install --upgrade pip
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

This installs all packages from requirements.txt (~2GB download).

### 5. Verify Installation
```powershell
pip list
python -c "import fastapi; import torch; import transformers; print('✓ All imports OK')"
```

## 🔄 Dependency Management

### Update All Dependencies
```powershell
pip install --upgrade -r requirements.txt
```

### Update Specific Package
```powershell
pip install --upgrade torch
```

### Check Installed Versions
```powershell
pip show torch transformers fastapi
```

### Generate Updated Requirements
```powershell
pip freeze > requirements-full.txt
```

## 📦 Package Purposes Explained

### **FastAPI** (`fastapi`)
- Modern async web framework
- Auto-generated API documentation (Swagger UI at `/docs`)
- Built-in request validation
- Dependency injection
- WebSocket support

### **Uvicorn** (`uvicorn[standard]`)
- ASGI server (runs FastAPI apps)
- `[standard]` includes:
  - `httptools` - Fast HTTP parsing
  - `websockets` - WebSocket support
  - `watchfiles` - Auto-reload on code changes
  - `python-dotenv` - Load .env files

### **PyTorch** (`torch`)
- Deep learning framework
- Runs IndoBERT model
- CPU version recommended for production (smaller, faster install)
- GPU version for training (requires CUDA)

### **Transformers** (`transformers`)
- Hugging Face library
- Loads pre-trained models (IndoBERT)
- Tokenization
- Model inference

### **Hugging Face Hub** (`huggingface-hub`)
- Download models from hub.huggingface.co
- Auto-download on backend startup
- Requires `HF_TOKEN` for private repos

### **Pytesseract** (`pytesseract`)
- OCR for PNG/JPG images
- Extracts Indonesian + English text
- Requires Tesseract executable installed

### **python-docx** (`python-docx`)
- Parse DOCX documents
- Extract text from Word files
- Alternative to OCR for document input

### **Pydantic** (`pydantic`)
- Data validation
- Request/response models
- Type checking
- Auto-generated JSON schemas

## 🔧 Installation Variants

### CPU-Only PyTorch (Recommended for Production)
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**Advantages:**
- Smaller download (~200MB vs ~2GB)
- Faster installation
- Sufficient for inference
- Works on all machines

### GPU PyTorch (For Training/Development)
```powershell
# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Requirements:**
- NVIDIA GPU with CUDA support
- CUDA Toolkit installed
- cuDNN library

## 🌐 API Documentation

After starting the server, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'`
```powershell
pip uninstall pydantic pydantic-core -y
pip install pydantic==2.9.2 --force-reinstall
```

### Issue: PyTorch DLL error on Windows
```powershell
# Reinstall CPU version
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Issue: `uvicorn: command not found`
```powershell
# Ensure venv is activated
.venv\Scripts\Activate.ps1
# Reinstall uvicorn
pip install --force-reinstall uvicorn[standard]
```

### Issue: Tesseract not found
```powershell
# Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
# Then add to PATH or set:
$env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### Issue: Model not found
```powershell
# Option 1: Use local model
# Ensure files exist in: Model IndoBERT/models/indobert/

# Option 2: Configure Hugging Face auto-download
# Create .env file:
HF_MODEL_REPO=your-username/your-model-repo
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx
```

### Issue: Import errors from `src` module
```powershell
# Ensure you're in Backend/fastapi-app directory
cd Backend/fastapi-app
# The startup hook in main.py adds paths automatically
```

## 🔐 Environment Variables

Create `.env` file in `Backend/fastapi-app/`:

```env
# Hugging Face Model (optional)
HF_MODEL_REPO=your-username/indobert-model
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx

# Tesseract OCR (optional, if not in PATH)
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# Server Settings (optional)
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

Load with:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 📊 Performance Notes

### Memory Usage
- Base server: ~200MB
- With model loaded: ~1.5GB
- During inference: ~2GB peak

### Startup Time
- Cold start (download model): 2-5 minutes
- Warm start (model cached): 10-20 seconds
- Model loading: 5-10 seconds

### Response Times
- Text prediction: 100-300ms
- Image OCR + prediction: 1-3 seconds
- DOCX + prediction: 200-500ms

## 🧪 Testing

### Install Test Dependencies
```powershell
pip install pytest pytest-cov httpx
```

### Run Tests
```powershell
pytest tests/ -v
pytest tests/ --cov=app  # With coverage
```

## 🔗 Additional Resources

- **FastAPI Tutorial:** https://fastapi.tiangolo.com/tutorial
- **PyTorch Tutorials:** https://pytorch.org/tutorials
- **Transformers Docs:** https://huggingface.co/docs/transformers
- **Tesseract OCR:** https://github.com/tesseract-ocr/tesseract
- **Python-DOCX:** https://python-docx.readthedocs.io

## 📈 Production Deployment

### Using Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment-Specific Requirements
```powershell
# Development
pip install -r requirements.txt
pip install pytest black flake8

# Production
pip install -r requirements.txt --no-dev
```

## 🔒 Security Best Practices

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use environment variables** for secrets
3. **Keep dependencies updated** - Run `pip list --outdated`
4. **Scan for vulnerabilities** - Use `pip-audit`
5. **Use HTTPS in production** - Configure reverse proxy
6. **Validate all inputs** - Pydantic handles this automatically
7. **Rate limiting** - Use middleware for API rate limits
8. **CORS configuration** - Set allowed origins properly

## 📝 Maintenance Checklist

- [ ] Update dependencies monthly
- [ ] Check for security advisories
- [ ] Monitor model performance
- [ ] Review logs for errors
- [ ] Test backup/restore procedures
- [ ] Document API changes
- [ ] Keep README.md updated
