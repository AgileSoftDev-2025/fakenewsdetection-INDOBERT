Framework used: Next.js

Folder: `Frontend/nextjs-app`

Windows setup

1) Install dependencies

```powershell
cd "Frontend/nextjs-app"
npm install
```

2) Configure API URL (optional; default http://localhost:8000)

```powershell
Copy-Item .env.local.example .env.local
# edit .env.local if backend runs on a different URL/port
```

3) Run dev server

```powershell
npm run dev
```

Pages

- / → Home: form judul/isi, panggil POST /predict
- /history → tabel feedback
- /admin → tampilkan versi model (retrain optional di tahap berikutnya)