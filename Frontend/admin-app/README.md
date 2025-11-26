# FakeNewsDetector - Admin Dashboard

Panel administrasi untuk mengelola sistem deteksi hoax.

## 🚀 Cara Menjalankan

### 1. Setup Environment

Buat file `.env.local` dan isi dengan:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Install dependencies

```bash
npm install
```

### 3. Jalankan Backend (Port 8000)

```bash
cd ../../Backend/fastapi-app
uvicorn app.main:app --reload --port 8000
```

### 4. Jalankan Admin Dashboard (Port 3001)

```bash
npm run dev
```

### 5. Akses Dashboard

Buka browser di http://localhost:3001

## 📦 Teknologi

- **Next.js 14** - React Framework dengan App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **React** - UI Library

## 🔒 Keamanan

Dashboard admin berjalan di port **3001** yang terpisah dari aplikasi user (port 3000). Pastikan untuk menambahkan autentikasi sebelum deployment ke production.

## 📊 Fitur

- Dashboard overview dengan statistik real-time dari `feedback.csv`
- Animasi counter untuk statistik
- Auto-fetch data dari backend API
- Error handling dengan retry button
- Loading state
- Responsive design
- Manajemen sistem dan model

## 🔌 API Endpoints

Dashboard ini menggunakan endpoint berikut dari backend:

- `GET /admin/stats` - Mendapatkan statistik (total, hoax, valid) dari feedback.csv

## 📈 Data Source

Statistik diambil dari file `Model IndoBERT/data/feedback/feedback.csv` yang berisi:
- Total pengecekan berita
- Jumlah berita hoax terdeteksi
- Jumlah berita valid
- Persentase masing-masing
