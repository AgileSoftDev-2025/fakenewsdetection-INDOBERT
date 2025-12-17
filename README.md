# 🔍 Fake News Detection with IndoBERT

Sistem deteksi berita palsu (hoax) berbahasa Indonesia menggunakan model **IndoBERT** dengan interface web yang modern dan dashboard admin untuk manajemen model.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)](https://fastapi.tiangolo.com/)
[![IndoBERT](https://img.shields.io/badge/Model-IndoBERT-blue)](https://huggingface.co/indobenchmark/indobert-base-p1)

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Arsitektur Sistem](#-arsitektur-sistem)
- [Tech Stack](#-tech-stack)
- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Penggunaan](#-penggunaan)
- [Struktur Project](#-struktur-project)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Retrain Model](#-retrain-model)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

## ✨ Fitur Utama

### 🌐 Public Interface
- **Deteksi Berita Real-time**: Analisis teks berita dengan hasil confidence score
- **Multi-format Input**: Support teks langsung, file upload (.txt, .docx)
- **History Tracking**: Riwayat deteksi dengan filter dan pencarian
- **Feedback System**: User dapat memberikan feedback untuk meningkatkan model
- **Responsive Design**: UI modern dengan Tailwind CSS

### 👨‍💼 Admin Dashboard
- **System Monitoring**: Real-time monitoring status sistem dan model
- **Model Management**: Kelola versi model dengan metric-based activation
- **Retrain Progress**: Track progress retrain model dengan 8 tahap visualisasi
- **Manual Retrain**: Trigger retrain manual dengan GPU support (local only)
- **Feedback Review**: Review dan approve feedback untuk dataset training
- **Statistics Dashboard**: Visualisasi metrics dan performance model

### 🤖 Backend API
- **RESTful API**: FastAPI dengan automatic OpenAPI documentation
- **PostgreSQL Database**: Persistent storage untuk history dan feedback
- **Hugging Face Integration**: Model inference via HF Spaces
- **Background Tasks**: Async processing untuk retrain dan upload
- **CORS Support**: Cross-origin support untuk frontend apps

## 🏗️ Arsitektur Sistem

```
┌─────────────────┐         ┌─────────────────┐
│  Public Web App │         │  Admin Dashboard│
│   (Next.js)     │         │    (Next.js)    │
│  Port: 3000     │         │   Port: 3001    │
└────────┬────────┘         └────────┬────────┘
         │                           │
         └───────────┬───────────────┘
                     │
              ┌──────▼──────┐
              │   FastAPI   │
              │  Backend    │
              │  Port: 8000 │
              └──────┬──────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼────┐ ┌───▼────┐ ┌───▼────────┐
    │PostgreSQL│ │IndoBERT│ │ HF Space   │
    │ Database │ │ Local  │ │ Inference  │
    └──────────┘ └────────┘ └────────────┘
```

### Alur Retrain Model

1. **Local Training**: Model dilatih di laptop dengan GPU
2. **Upload to HF Hub**: Model hasil training diupload ke Hugging Face Repository
3. **HF Space Inference**: Public app menggunakan model dari HF Space untuk prediksi
4. **Metric Validation**: Model baru diaktifkan jika metrics memenuhi threshold

## 🛠️ Tech Stack

### Frontend
- **Next.js 14**: React framework dengan App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **SWR**: Data fetching dan caching
- **Recharts**: Data visualization

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Relational database
- **SQLAlchemy**: ORM untuk database operations
- **Transformers**: Hugging Face library untuk NLP
- **IndoBERT**: Pre-trained Indonesian BERT model

### Machine Learning
- **PyTorch**: Deep learning framework
- **Hugging Face Transformers**: Model training & inference
- **IndoBERT Base**: `indobenchmark/indobert-base-p1`
- **Dataset**: Custom labeled Indonesian news dataset

### DevOps & Deployment
- **Docker**: Containerization (optional)
- **Vercel**: Frontend hosting
- **Railway/Render**: Backend hosting (recommended)
- **Git**: Version control

## 📦 Prasyarat

- **Python 3.8+** (Backend & Model)
- **Node.js 18+** (Frontend)
- **PostgreSQL 13+** (Database)
- **GPU** (Optional, untuk retrain model)
- **Git** (Version control)

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/AgileSoftDev-2025/fakenewsdetection-INDOBERT.git
cd fakenewsdetection-INDOBERT
```

### 2. Setup Database

Buat database PostgreSQL:

```sql
CREATE DATABASE fakenews_db;
CREATE USER fakenews_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fakenews_db TO fakenews_user;
```

### 3. Setup Backend

```bash
cd Backend/fastapi-app

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env file dengan database credentials

# Run database migrations
python migrate_to_db.py

# Start backend server
uvicorn app.main:app --reload --port 8000
```

### 4. Setup Admin Dashboard

```bash
cd Frontend/admin-app

# Install dependencies
npm install

# Setup environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Admin dashboard akan berjalan di: http://localhost:3001

### 5. Setup Public App

```bash
cd Frontend/nextjs-app

# Install dependencies
npm install

# Setup environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Public app akan berjalan di: http://localhost:3000

## 📖 Penggunaan

### Public Interface

1. Buka http://localhost:3000
2. Masukkan teks berita atau upload file
3. Klik "Deteksi Berita"
4. Lihat hasil analisis dengan confidence score
5. (Optional) Berikan feedback jika hasil tidak akurat

### Admin Dashboard

1. Buka http://localhost:3001
2. Dashboard akan menampilkan:
   - System status (Backend, Database, Model)
   - Model performance metrics
   - Retrain progress (jika sedang berjalan)
3. **Mulai Retrain**:
   - Klik tombol "🚀 Mulai Retrain"
   - Monitor progress real-time
   - Model akan otomatis terupload ke HF Hub
4. **Kelola Model**:
   - Navigate ke `/list-model`
   - Lihat semua versi model
   - Activate model berdasarkan metrics

## 📁 Struktur Project

```
fakenewsdetection-INDOBERT/
├── Backend/
│   └── fastapi-app/
│       ├── app/
│       │   ├── api/          # API endpoints
│       │   ├── services/     # Business logic
│       │   ├── database.py   # DB configuration
│       │   ├── models.py     # SQLAlchemy models
│       │   └── main.py       # FastAPI app
│       └── requirements.txt
│
├── Frontend/
│   ├── admin-app/            # Admin dashboard (port 3001)
│   │   ├── app/
│   │   │   ├── page.tsx      # Dashboard home
│   │   │   └── list-model/   # Model management
│   │   ├── components/       # React components
│   │   └── package.json
│   │
│   └── nextjs-app/           # Public interface (port 3000)
│       ├── app/
│       │   └── page.tsx      # Main detection page
│       ├── components/
│       └── package.json
│
├── Model IndoBERT/
│   ├── data/
│   │   ├── retrain_progress.json  # Retrain state
│   │   └── feedback/              # User feedback data
│   ├── models/
│   │   ├── indobert/              # Active model
│   │   └── indobert_versions/     # Model versions
│   └── scripts/
│       ├── auto_retrain_indobert.py  # Retrain script
│       └── predict_text.py           # Local inference
│
├── .gitignore
└── README.md
```

## 🔌 API Documentation

### Health Check

```http
GET /
```

Response: `{ "status": "ok" }`

### Detect News

```http
POST /api/detect
Content-Type: application/json

{
  "text": "Teks berita yang akan dianalisis..."
}
```

Response:
```json
{
  "label": "VALID",
  "confidence": 0.9234,
  "created_at": "2025-12-17T10:30:00"
}
```

### Get Detection History

```http
GET /api/history?limit=10&offset=0
```

### Submit Feedback

```http
POST /api/feedback
Content-Type: application/json

{
  "text": "Teks berita",
  "predicted_label": "VALID",
  "correct_label": "HOAX"
}
```

### Retrain Endpoints (Admin Only)

- `GET /api/retrain/progress` - Get retrain progress
- `POST /api/retrain/start` - Start manual retrain
- `POST /api/retrain/reset` - Reset stuck progress

### Model Management

- `GET /api/models/versions` - List all model versions
- `POST /api/models/activate/{version}` - Activate model version

**Full API Documentation**: http://localhost:8000/docs (Swagger UI)

## 🌍 Deployment

### Frontend (Vercel)

#### Deploy Admin Dashboard

1. Buka [Vercel Dashboard](https://vercel.com)
2. Import repository: `AgileSoftDev-2025/fakenewsdetection-INDOBERT`
3. Konfigurasi:
   - **Framework**: Next.js
   - **Root Directory**: `Frontend/admin-app`
   - **Build Command**: `npm run build`
   - **Environment Variables**:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend-url.com
     ```
4. Deploy

#### Deploy Public App

1. Import repository yang sama ke Vercel
2. Konfigurasi:
   - **Framework**: Next.js
   - **Root Directory**: `Frontend/nextjs-app`
   - **Build Command**: `npm run build`
   - **Environment Variables**:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend-url.com
     ```
3. Deploy

### Backend (Railway/Render)

#### Option 1: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd Backend/fastapi-app
railway init
railway up
```

#### Option 2: Render

1. Buat Web Service baru di [Render](https://render.com)
2. Connect repository
3. Konfigurasi:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `Backend/fastapi-app`
4. Tambahkan Environment Variables
5. Deploy

### Update CORS

Setelah deploy, update CORS di `Backend/fastapi-app/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://admin-app-xxx.vercel.app",
        "https://nextjs-app-xxx.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔄 Retrain Model

### Prerequisites

- GPU dengan CUDA support (recommended)
- Dataset feedback minimum 100 samples
- Disk space minimum 10GB

### Langkah Retrain

1. **Persiapan Data**:
   - User feedback akan tersimpan di `Model IndoBERT/data/feedback/`
   - Pastikan ada minimum 100 feedback ter-approve

2. **Mulai Retrain** (via Admin Dashboard):
   - Buka http://localhost:3001
   - Klik tombol "🚀 Mulai Retrain"
   - Monitor progress real-time

3. **Tahapan Retrain**:
   - ✅ Preparing data (10%)
   - ✅ Loading model (20%)
   - ✅ Training epoch 1/3 (40%)
   - ✅ Training epoch 2/3 (60%)
   - ✅ Training epoch 3/3 (80%)
   - ✅ Evaluating (90%)
   - ✅ Uploading to HF Hub (95%)
   - ✅ Completed (100%)

4. **Post-Retrain**:
   - Model otomatis terupload ke Hugging Face Hub
   - Metrics akan divalidasi
   - Model diaktifkan jika metrics > threshold

### Manual Retrain (CLI)

```bash
cd "Model IndoBERT/scripts"
python auto_retrain_indobert.py
```

### Reset Progress (jika stuck)

```bash
# Via Admin Dashboard
curl -X POST http://localhost:8000/api/retrain/reset

# Atau manual edit
# Model IndoBERT/data/retrain_progress.json
```

## 🤝 Kontribusi

Kontribusi sangat diterima! Berikut cara berkontribusi:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Guidelines

- Follow existing code style
- Write clear commit messages
- Update documentation
- Add tests for new features
- Ensure all tests pass before PR

## 📄 Lisensi

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Tim Pengembang

- **AgileSoftDev-2025** - *Initial work*

## 🙏 Acknowledgments

- [IndoBERT](https://github.com/indobenchmark/indonlu) - Pre-trained Indonesian BERT model
- [Hugging Face](https://huggingface.co/) - Model hosting and inference
- [Next.js](https://nextjs.org/) - React framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework

## 📞 Support

Jika ada pertanyaan atau issues:
- **GitHub Issues**: [Create an issue](https://github.com/AgileSoftDev-2025/fakenewsdetection-INDOBERT/issues)
- **Email**: support@agilesoftdev.com (coming soon)

## 🔮 Roadmap

- [ ] Multi-language support (English, Malay)
- [ ] Real-time news monitoring
- [ ] Browser extension
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] API rate limiting
- [ ] User authentication system
- [ ] Automated A/B testing for models

---

**Made with ❤️ by AgileSoftDev-2025**