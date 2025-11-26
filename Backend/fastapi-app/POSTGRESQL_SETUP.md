# PostgreSQL Lokal Setup Guide

Panduan instalasi dan konfigurasi PostgreSQL lokal untuk aplikasi Fake News Detection.

---

## 📋 Prasyarat

- Windows 10/11
- Hak akses Administrator
- Minimal 500 MB disk space

---

## 🔧 Instalasi PostgreSQL

### Opsi 1: Instalasi dengan Installer (Recommended)

1. **Download PostgreSQL**
   - Kunjungi: https://www.postgresql.org/download/windows/
   - Download PostgreSQL 15 atau 16 (versi terbaru)
   - Ukuran: ~250 MB

2. **Jalankan Installer**
   - Run as Administrator
   - Installation Directory: `C:\Program Files\PostgreSQL\16` (default)
   - Komponen yang diinstall:
     - ✅ PostgreSQL Server
     - ✅ pgAdmin 4 (GUI tool)
     - ✅ Command Line Tools
     - ❌ Stack Builder (optional)

3. **Konfigurasi saat Instalasi**
   - **Port**: `5432` (default)
   - **Locale**: `Indonesian, Indonesia` atau `Default locale`
   - **Password superuser (postgres)**: **SIMPAN PASSWORD INI!**
     - Contoh: `postgres123` (untuk development)
     - Untuk production: gunakan password yang kuat

4. **Selesai**
   - Klik Finish
   - PostgreSQL service akan berjalan otomatis

### Opsi 2: Menggunakan Docker (Alternative)

```powershell
# Pull PostgreSQL image
docker pull postgres:16

# Run PostgreSQL container
docker run --name fakenews-postgres `
  -e POSTGRES_PASSWORD=postgres123 `
  -e POSTGRES_DB=fakenews_detection `
  -p 5432:5432 `
  -d postgres:16

# Verify running
docker ps
```

---

## 🗄️ Setup Database

### Metode 1: Menggunakan pgAdmin 4 (GUI)

1. **Buka pgAdmin 4**
   - Start Menu > pgAdmin 4
   - Masukkan master password (buat jika pertama kali)

2. **Connect ke Server**
   - Expand: Servers > PostgreSQL 16
   - Masukkan password postgres yang dibuat saat instalasi

3. **Buat Database Baru**
   - Klik kanan pada "Databases" > Create > Database
   - Database name: `fakenews_detection`
   - Owner: `postgres`
   - Click "Save"

4. **Buat Table**
   - Klik kanan database `fakenews_detection` > Query Tool
   - Copy dan paste SQL di bawah:

```sql
-- Create feedback table
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    timestamp BIGINT NOT NULL,
    model_name VARCHAR(50),
    model_version VARCHAR(20),
    text_length INTEGER,
    prediction INTEGER CHECK (prediction IN (0, 1)),
    prob_hoax FLOAT,
    confidence FLOAT,
    user_label INTEGER CHECK (user_label IN (0, 1)),
    agreement VARCHAR(20),
    raw_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_feedback_prediction ON feedback(prediction);
CREATE INDEX idx_feedback_created_at ON feedback(created_at);
CREATE INDEX idx_feedback_timestamp ON feedback(timestamp);

-- Create view for quick stats
CREATE VIEW feedback_stats AS
SELECT
    COUNT(*) as total_checks,
    COUNT(CASE WHEN prediction = 1 THEN 1 END) as hoax_count,
    COUNT(CASE WHEN prediction = 0 THEN 1 END) as valid_count,
    ROUND(COUNT(CASE WHEN prediction = 1 THEN 1 END)::NUMERIC / NULLIF(COUNT(*), 0) * 100, 1) as hoax_percentage,
    ROUND(COUNT(CASE WHEN prediction = 0 THEN 1 END)::NUMERIC / NULLIF(COUNT(*), 0) * 100, 1) as valid_percentage
FROM feedback;
```

   - Klik Execute (⚡ icon atau F5)
   - Verify: "Query returned successfully"

### Metode 2: Menggunakan Command Line (psql)

```powershell
# Buka PowerShell/CMD
# Navigate ke PostgreSQL bin folder
cd "C:\Program Files\PostgreSQL\16\bin"

# Login ke PostgreSQL
.\psql -U postgres

# Masukkan password postgres

# Create database
CREATE DATABASE fakenews_detection;

# Connect to database
\c fakenews_detection

# Run SQL script (copy-paste SQL dari Metode 1)
# Atau import dari file:
\i C:\path\to\schema.sql

# Verify tables
\dt

# Exit
\q
```

---

## 🔌 Test Koneksi

### Test dengan pgAdmin 4

1. Buka pgAdmin 4
2. Expand: Servers > PostgreSQL 16 > Databases > fakenews_detection > Schemas > public > Tables
3. Klik kanan pada `feedback` > View/Edit Data > All Rows
4. Jika muncul tabel kosong = **Success!** ✅

### Test dengan Python

```powershell
# Install psycopg2
pip install psycopg2-binary

# Test connection
python
```

```python
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="fakenews_detection",
        user="postgres",
        password="postgres123"  # Ganti dengan password Anda
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

---

## ⚙️ Konfigurasi Aplikasi

### 1. Update `.env` File

```powershell
cd Backend/fastapi-app
```

Edit file `.env` (atau buat dari `.env.example`):

```env
# Database Configuration
USE_DATABASE=false  # Set false dulu untuk testing

# PostgreSQL Local Connection
# Format: postgresql://username:password@localhost:5432/database_name
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/fakenews_detection
```

**Ganti `postgres123` dengan password PostgreSQL Anda!**

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

Output expected:
```
Installing collected packages: sqlalchemy, psycopg2-binary, alembic
Successfully installed...
```

### 3. Test Database Connection

```powershell
python
```

```python
from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT version()"))
    print(result.fetchone())
# Output: PostgreSQL 16.x on x86_64...
```

---

## 📊 Migration dari CSV

### 1. Jalankan Migration Script

```powershell
# Dari folder Backend/fastapi-app
python migrate_to_db.py
```

**Expected Output:**
```
======================================================================
MIGRATING FEEDBACK.CSV TO POSTGRESQL
======================================================================

📊 Database: localhost:5432/fakenews_detection

1️⃣  Creating tables...
   ✅ Tables created successfully
   ✅ Found CSV: C:\...\feedback.csv

2️⃣  Reading CSV data...
   ✅ Read 10 records from CSV

3️⃣  Inserting records into database...
   ✅ Successfully inserted 10 records

4️⃣  Verifying migration...
   ✅ Total records in database: 10
   ✅ Hoax: 5
   ✅ Valid: 5

✅ MIGRATION COMPLETED SUCCESSFULLY!
```

### 2. Verify di pgAdmin

1. Buka pgAdmin 4
2. fakenews_detection > Schemas > public > Tables > feedback
3. Right-click > View/Edit Data > All Rows
4. Harus muncul data dari CSV

---

## 🚀 Enable Database Mode

### 1. Update `.env`

```env
USE_DATABASE=true  # ✅ Enable database mode
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/fakenews_detection
```

### 2. Restart FastAPI Server

```powershell
# Stop server (Ctrl+C jika masih running)

# Restart
uvicorn app.main:app --reload --port 8000
```

### 3. Test Admin Dashboard

1. Buka browser: http://localhost:3001
2. Cek stats dashboard
3. Harus menampilkan data dari PostgreSQL

---

## 🔍 Troubleshooting

### Error: "Connection refused"

**Penyebab**: PostgreSQL service tidak jalan

**Solusi**:
```powershell
# Check service status
Get-Service postgresql*

# Start service
Start-Service postgresql-x64-16

# Atau via Services.msc:
# 1. Win+R > services.msc
# 2. Cari "postgresql-x64-16"
# 3. Right-click > Start
```

### Error: "password authentication failed"

**Penyebab**: Password salah di DATABASE_URL

**Solusi**:
1. Verify password PostgreSQL Anda
2. Update `.env` dengan password yang benar
3. Restart aplikasi

### Error: "database 'fakenews_detection' does not exist"

**Solusi**:
```powershell
# Login ke psql
cd "C:\Program Files\PostgreSQL\16\bin"
.\psql -U postgres

# Create database
CREATE DATABASE fakenews_detection;
\q
```

### Error: "relation 'feedback' does not exist"

**Solusi**: Jalankan SQL CREATE TABLE dari Metode 1 atau 2 di atas

### Port 5432 sudah digunakan

**Solusi 1**: Stop service lain yang menggunakan port 5432
```powershell
# Cek apa yang menggunakan port 5432
netstat -ano | findstr :5432

# Kill process by PID
taskkill /PID <PID> /F
```

**Solusi 2**: Ubah port PostgreSQL
1. Edit `postgresql.conf`
2. Ubah `port = 5432` → `port = 5433`
3. Restart PostgreSQL service
4. Update `.env`: `DATABASE_URL=postgresql://...@localhost:5433/...`

---

## 📈 Monitoring & Maintenance

### View Database Size

```sql
SELECT pg_size_pretty(pg_database_size('fakenews_detection'));
```

### View Table Stats

```sql
SELECT * FROM feedback_stats;
```

### View Recent Entries

```sql
SELECT id, model_name, prediction, created_at
FROM feedback
ORDER BY created_at DESC
LIMIT 10;
```

### Backup Database

```powershell
# Full backup
cd "C:\Program Files\PostgreSQL\16\bin"
.\pg_dump -U postgres -d fakenews_detection -F c -f C:\backup\fakenews_backup.dump

# Restore
.\pg_restore -U postgres -d fakenews_detection C:\backup\fakenews_backup.dump
```

### Optimize Performance

```sql
-- Analyze table for query optimization
ANALYZE feedback;

-- Vacuum to reclaim space
VACUUM ANALYZE feedback;
```

---

## 🎯 Development vs Production

### Development (Local CSV)
```env
USE_DATABASE=false
# Tidak perlu DATABASE_URL
```
- Fast untuk testing
- Tidak perlu PostgreSQL running
- Data di `feedback.csv`

### Production (PostgreSQL)
```env
USE_DATABASE=true
DATABASE_URL=postgresql://postgres:password@localhost:5432/fakenews_detection
```
- Production-ready
- ACID compliance
- Concurrent access
- Better performance

---

## 📚 Resources

- **pgAdmin 4**: GUI tool untuk manage PostgreSQL
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **psycopg2 Docs**: https://www.psycopg.org/docs/

---

## ✅ Quick Checklist

Setup complete jika:

- [ ] PostgreSQL installed dan running (service active)
- [ ] Database `fakenews_detection` created
- [ ] Table `feedback` created dengan schema yang benar
- [ ] Connection test berhasil (Python/pgAdmin)
- [ ] Migration script executed successfully
- [ ] `.env` configured dengan DATABASE_URL yang benar
- [ ] Admin dashboard menampilkan data dari PostgreSQL

**Selesai!** Database PostgreSQL lokal siap digunakan. 🎉
