# FakeNewsDetector - Sistem Dual Port

Sistem fake news detection dengan arsitektur dual port untuk memisahkan akses user dan admin.

## 🏗️ Arsitektur Sistem

### Port Configuration

| Aplikasi | Port | Akses | Deskripsi |
|----------|------|-------|-----------|
| **User App** | 3000 | Public | Aplikasi untuk end-user melakukan pengecekan berita |
| **Admin Dashboard** | 3001 | Admin Only | Panel administrasi untuk mengelola sistem |
| **Backend API** | 8000 | Internal | FastAPI backend untuk kedua aplikasi |

## 📦 Struktur Folder

```
Frontend/
├── nextjs-app/          # User Application (Port 3000)
│   ├── app/
│   ├── components/
│   ├── package.json
│   └── README.md
│
└── admin-app/           # Admin Dashboard (Port 3001)
    ├── app/
    ├── components/
    ├── package.json
    └── README.md
```

## 🚀 Cara Menjalankan

### 1. Backend API (Port 8000)

```bash
cd Backend/fastapi-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. User App (Port 3000)

```bash
cd Frontend/nextjs-app
npm install
npm run dev
```

Akses di: http://localhost:3000

### 3. Admin Dashboard (Port 3001)

```bash
cd Frontend/admin-app
npm install
npm run dev
```

Akses di: http://localhost:3001

## 🔒 Keamanan & Deployment

### Development

- User app (3000) dan Admin app (3001) berjalan terpisah
- Kedua app menggunakan backend yang sama (8000)

### Production Recommendations

1. **Admin Dashboard (Port 3001)**
   - Deploy di subdomain terpisah: `admin.yourdomain.com`
   - Tambahkan autentikasi (JWT, OAuth, dll)
   - Gunakan middleware untuk authorization
   - Whitelist IP jika memungkinkan
   - Enable HTTPS/SSL

2. **User App (Port 3000)**
   - Deploy di domain utama: `yourdomain.com`
   - Public access
   - Rate limiting untuk API calls
   - Enable HTTPS/SSL

3. **Backend API (Port 8000)**
   - Deploy sebagai internal service
   - Hanya bisa diakses dari frontend apps
   - CORS configuration yang ketat
   - API key authentication

## 🛠️ Environment Variables

### Backend (.env)
```env
HF_MODEL_REPO=Davidbio/fakenewsdetection-indobert
HF_TOKEN=your_huggingface_token_here
```

### User App (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Admin App (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ADMIN_SECRET=your_admin_secret_here
```

## 📊 Fitur Admin Dashboard

- ✅ Dashboard overview dengan statistik real-time
- ✅ Animasi counter untuk statistik
- ✅ Responsive design
- ✅ Manajemen sistem dan model
- 🔄 Dataset management (coming soon)
- 🔄 Analytics dan reporting (coming soon)
- 🔄 User management (coming soon)

## 📝 Development Workflow

1. **Develop Backend** → Test di port 8000
2. **Develop User App** → Test di port 3000
3. **Develop Admin Dashboard** → Test di port 3001
4. Semua berjalan bersamaan untuk testing end-to-end

## 🧪 Testing

Jalankan semua services:

```bash
# Terminal 1 - Backend
cd Backend/fastapi-app
uvicorn app.main:app --reload --port 8000

# Terminal 2 - User App  
cd Frontend/nextjs-app
npm run dev

# Terminal 3 - Admin Dashboard
cd Frontend/admin-app
npm run dev
```

Kemudian test:
- User App: http://localhost:3000
- Admin Dashboard: http://localhost:3001
- API Docs: http://localhost:8000/docs

## 📦 Build untuk Production

### User App
```bash
cd Frontend/nextjs-app
npm run build
npm run start  # Runs on port 3000
```

### Admin Dashboard
```bash
cd Frontend/admin-app
npm run build
npm run start  # Runs on port 3001
```

## 🔐 Menambahkan Autentikasi Admin

Untuk menambahkan autentikasi di admin dashboard, buat middleware:

```typescript
// Frontend/admin-app/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('admin_token')?.value;
  
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|login).*)'],
};
```

## 📚 Dokumentasi Lengkap

- [Backend README](Backend/README.md)
- [User App README](Frontend/nextjs-app/README.md)
- [Admin Dashboard README](Frontend/admin-app/README.md)
- [BDD Testing Guide](tests/bdd/BDD_TESTING_GUIDE.md)
- [Hugging Face Setup](Backend/fastapi-app/HUGGINGFACE_SETUP.md)
