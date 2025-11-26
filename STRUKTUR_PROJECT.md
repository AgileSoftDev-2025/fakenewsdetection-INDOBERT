# Struktur Project FakeNewsDetector

## 📁 Struktur Folder Utama

```
fakenewsdetection-INDOBERT/
├── Backend/                    # Backend FastAPI
│   └── fastapi-app/
│       ├── app/
│       │   ├── api/           # API endpoints
│       │   │   └── admin.py   # Admin endpoints (model management, stats)
│       │   ├── database.py    # Database connection
│       │   ├── models.py      # SQLAlchemy models
│       │   └── main.py        # FastAPI app entry point
│       └── src/
│           └── services/
│               └── model_registry.py  # Model version registry
│
├── Frontend/
│   ├── admin-app/             # Admin Dashboard (Next.js - Port 3001)
│   │   ├── app/
│   │   │   ├── list-model/    # Model selection page
│   │   │   │   ├── page.tsx
│   │   │   │   └── styles.module.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx       # Admin dashboard
│   │   └── components/
│   │       └── SystemGrid.tsx # Dashboard overview cards
│   │
│   └── nextjs-app/            # User App (Next.js - Port 3000)
│       ├── app/
│       │   ├── analisis-file/ # File upload analysis
│       │   ├── analisis-text/ # Text input analysis
│       │   ├── hasil-analisis/# Analysis result page
│       │   ├── layout.tsx
│       │   └── page.tsx       # User homepage
│       └── components/
│
├── Model IndoBERT/            # ML Model & Data
│   ├── data/
│   │   ├── feedback/          # User feedback data
│   │   ├── processed/         # Preprocessed datasets
│   │   └── raw/              # Raw datasets
│   ├── models/
│   │   ├── indobert/         # IndoBERT model files
│   │   └── indobert_versions/# Model version registry
│   │       └── registry.json
│   ├── scripts/
│   │   └── predict_text.py   # Prediction script
│   └── src/
│       ├── modeling/
│       │   ├── predict.py    # Prediction logic
│       │   └── train.py      # Training logic
│       └── services/
│
├── tests/                     # Unit & integration tests
├── bdd-testing-berita/       # BDD tests (Behave)
└── UI/                       # UI mockups & screenshots
```

## 🚀 Port Configuration

- **Backend**: `http://localhost:8000`
- **User App**: `http://localhost:3000`
- **Admin App**: `http://localhost:3001`

## 📝 File Penting

### Backend
- `Backend/fastapi-app/app/api/admin.py` - Endpoints untuk:
  - `/model/version` - Get current model version
  - `/api/models` - List all models with metrics
  - `/api/models/active` - Get active model with metrics
  - `/api/models/{version}/activate` - Activate model
  - `/api/models/deactivate` - Deactivate model
  - `/admin/stats` - Get feedback statistics

### Frontend Admin
- `Frontend/admin-app/app/page.tsx` - Dashboard admin
- `Frontend/admin-app/app/list-model/page.tsx` - Model selection page
- `Frontend/admin-app/components/SystemGrid.tsx` - Dashboard cards

### Frontend User
- `Frontend/nextjs-app/app/page.tsx` - Homepage user
- `Frontend/nextjs-app/app/analisis-text/page.tsx` - Text analysis
- `Frontend/nextjs-app/app/analisis-file/page.tsx` - File analysis
- `Frontend/nextjs-app/app/hasil-analisis/page.tsx` - Results page

### Model
- `Model IndoBERT/models/indobert_versions/registry.json` - Model version registry
- `Model IndoBERT/src/modeling/predict.py` - Prediction engine

## 🔧 Environment Variables

### Backend (.env)
```
USE_DATABASE=false
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📦 Dependencies

### Backend
- FastAPI 0.115.0
- Uvicorn
- PyTorch
- Transformers
- SQLAlchemy (optional, database mode)

### Frontend
- Next.js 14.2.10
- React 18.3.1
- TypeScript
- Tailwind CSS

## 🎯 Fitur Utama

### Admin Dashboard
1. **System Overview**
   - Versi model aktif
   - Tombol update model

2. **Performa Model**
   - Akurasi
   - Presisi
   - Recall
   - F1-Score

3. **List Model Page**
   - Lihat semua model tersedia
   - Aktivasi/deaktivasi model
   - Lihat metrik per model

### User App
1. **Analisis Text** - Input manual berita
2. **Analisis File** - Upload file CSV
3. **Hasil Analisis** - Tampil hasil prediksi
4. **Feedback** - User dapat memberikan feedback

## 🗂️ File yang Dihapus (Cleanup)

File-file berikut sudah dihapus karena tidak relevan:
- ✅ `Frontend/src/` - Sudah migrate ke admin-app
- ✅ `Frontend/index.html` - Tidak diperlukan (Next.js)
- ✅ `Frontend/vite.config.ts` - Tidak diperlukan (Next.js)
- ✅ `Frontend/tsconfig.app.json` - Tidak diperlukan (Next.js)
- ✅ `Frontend/eslint.config.js` - Tidak diperlukan (Next.js)
- ✅ `MERGE_FIXES.md` - Dokumentasi sementara
- ✅ `DUAL_PORT_SETUP.md` - Dokumentasi sementara
- ✅ `jbkfa` - File tidak jelas

## 📖 Cara Menjalankan

### Backend
```bash
cd Backend/fastapi-app
uvicorn app.main:app --reload --port 8000
```

### User App
```bash
cd Frontend/nextjs-app
npm run dev
```

### Admin App
```bash
cd Frontend/admin-app
npm run dev
```
