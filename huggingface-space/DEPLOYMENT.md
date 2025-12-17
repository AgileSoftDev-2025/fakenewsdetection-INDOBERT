# 📦 Hugging Face Space - IndoBERT Fake News Detection

Folder ini berisi setup lengkap untuk deploy model IndoBERT ke Hugging Face Spaces menggunakan Docker.

## 📁 Struktur File

```
huggingface-space/
├── app.py              # Aplikasi Gradio untuk interface
├── Dockerfile          # Docker configuration untuk HF Spaces
├── requirements.txt    # Python dependencies
├── README.md          # Metadata untuk HF Space (YAML header)
├── .gitignore         # Git ignore rules
├── models/            # [Opsional] Model files lokal
│   └── indobert/
└── DEPLOYMENT.md      # Panduan deployment (file ini)
```

## 🚀 Cara Deploy ke Hugging Face Spaces

### Opsi 1: Upload Langsung via Web UI

1. **Buat Space Baru**
   - Buka https://huggingface.co/new-space
   - Pilih nama untuk Space Anda (contoh: `indobert-fakenews`)
   - Pilih SDK: **Docker**
   - Pilih License: **MIT**
   - Klik "Create Space"

2. **Upload Files**
   - Upload semua file dari folder `huggingface-space/`:
     - `app.py`
     - `Dockerfile`
     - `requirements.txt`
     - `README.md` (penting! berisi metadata YAML)
   - **Jangan** upload folder `models/` jika modelnya besar

3. **Konfigurasi Model**
   
   Ada 2 cara:
   
   **A. Load dari HuggingFace Hub (Recommended)**
   - Upload model Anda ke HF Hub terlebih dahulu
   - Set environment variable di Space settings:
     ```
     HF_MODEL_REPO=your-username/indobert-fakenews-model
     ```
   
   **B. Upload Model Files**
   - Buat folder `models/indobert/` di Space
   - Upload semua file model (config.json, pytorch_model.bin, dll)

4. **Build & Deploy**
   - HF Spaces akan otomatis build Docker image
   - Tunggu hingga status berubah menjadi "Running"
   - Space Anda akan tersedia di: `https://huggingface.co/spaces/your-username/indobert-fakenews`

### Opsi 2: Deploy via Git

1. **Clone Space Repository**
   ```bash
   git clone https://huggingface.co/spaces/your-username/indobert-fakenews
   cd indobert-fakenews
   ```

2. **Copy Files**
   ```bash
   # Copy semua file dari folder huggingface-space
   cp ../huggingface-space/* .
   ```

3. **Add & Commit**
   ```bash
   git add .
   git commit -m "Initial commit: IndoBERT Fake News Detection"
   git push
   ```

4. **Upload Model (Opsional)**
   ```bash
   # Jika ingin upload model files
   git lfs install
   git lfs track "*.bin"
   git lfs track "*.safetensors"
   
   # Copy model files
   mkdir -p models/indobert
   cp -r ../../Model\ IndoBERT/models/indobert/* models/indobert/
   
   git add models/
   git commit -m "Add model files"
   git push
   ```

### Opsi 3: Deploy via Hugging Face CLI

1. **Install HF CLI**
   ```bash
   pip install huggingface-hub[cli]
   ```

2. **Login**
   ```bash
   huggingface-cli login
   ```

3. **Create & Push Space**
   ```bash
   cd huggingface-space
   
   # Create space
   huggingface-cli repo create indobert-fakenews --type space --space_sdk docker
   
   # Initialize git
   git init
   git add .
   git commit -m "Initial commit"
   
   # Add remote dan push
   git remote add origin https://huggingface.co/spaces/your-username/indobert-fakenews
   git push -u origin main
   ```

## ⚙️ Environment Variables

Set di Space Settings → Variables and Secrets:

| Variable | Description | Required |
|----------|-------------|----------|
| `HF_MODEL_REPO` | HuggingFace repo untuk model (e.g., `username/model-name`) | No |
| `HF_TOKEN` | Token untuk private repos | No (jika model private) |

## 🔧 Konfigurasi Hardware

Di Space Settings, Anda bisa upgrade hardware:

- **Free Tier**: CPU (2 vCPU, 16GB RAM) - Cukup untuk inference
- **Paid Tier**: 
  - T4 GPU: Lebih cepat, cocok untuk model besar
  - A10G GPU: Untuk production dengan traffic tinggi

## 📝 Testing Lokal

Sebelum deploy, test dulu secara lokal:

```bash
cd huggingface-space

# Install dependencies
pip install -r requirements.txt

# Run aplikasi
python app.py
```

Buka browser: http://localhost:7860

## 🐳 Test Docker Lokal

```bash
cd huggingface-space

# Build image
docker build -t indobert-fakenews .

# Run container
docker run -p 7860:7860 indobert-fakenews
```

Buka browser: http://localhost:7860

## 📊 Upload Model ke Hugging Face Hub

Jika ingin model di-host di HF Hub (recommended):

```bash
# Install transformers
pip install transformers huggingface-hub

# Login
huggingface-cli login

# Upload model
python upload_model.py
```

Buat file `upload_model.py`:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Path ke model lokal
local_model_path = "../Model IndoBERT/models/indobert"

# Load model
tokenizer = AutoTokenizer.from_pretrained(local_model_path)
model = AutoModelForSequenceClassification.from_pretrained(local_model_path)

# Upload ke HF Hub
repo_name = "your-username/indobert-fakenews-model"
tokenizer.push_to_hub(repo_name)
model.push_to_hub(repo_name)

print(f"Model uploaded to: https://huggingface.co/{repo_name}")
```

## 🎨 Customization

### Mengubah Theme Gradio

Edit `app.py`:

```python
# Theme options: Soft, Base, Glass, Monochrome, Default
demo = gr.Blocks(theme=gr.themes.Glass())
```

### Menambah Contoh Teks

Edit array `examples` di `app.py`:

```python
examples = [
    ["Teks berita pertama..."],
    ["Teks berita kedua..."],
]
```

### Mengubah Port

Edit di `Dockerfile`:

```dockerfile
ENV GRADIO_SERVER_PORT=7860
EXPOSE 7860
```

## 🔍 Troubleshooting

### Build Failed

1. Cek logs di Space
2. Pastikan semua dependencies ada di `requirements.txt`
3. Verifikasi Dockerfile syntax

### Model Not Loading

1. Cek path model di `app.py`
2. Verifikasi `HF_MODEL_REPO` environment variable
3. Cek HF_TOKEN jika model private

### Out of Memory

1. Reduce batch size
2. Upgrade ke GPU instance
3. Optimize model (quantization, distillation)

### Slow Loading

1. Upload model ke HF Hub daripada include di Space
2. Use model caching
3. Upgrade hardware

## 📚 Resources

- [HF Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://gradio.app/docs)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🆘 Support

Jika ada masalah:
1. Cek HF Spaces community forum
2. Buka issue di repository
3. Kontak maintainer

---

**Happy Deploying! 🚀**
