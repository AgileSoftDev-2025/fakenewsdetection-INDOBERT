# Setup PostgreSQL Database untuk Fake News Detection

## Status Saat Ini
✅ PostgreSQL 18 terinstall dan running
⏳ Perlu setup database dan koneksi

## Langkah-langkah Setup

### 1. Buka pgAdmin 4 atau psql

**Opsi A: Menggunakan pgAdmin 4 (GUI - Recommended)**
1. Buka **pgAdmin 4** dari Start Menu
2. Masukkan master password (jika diminta)
3. Connect ke **PostgreSQL 18** server
4. Masukkan password postgres

**Opsi B: Menggunakan psql (Command Line)**
```powershell
cd "C:\Program Files\PostgreSQL\18\bin"
.\psql -U postgres
# Masukkan password postgres saat diminta
```

### 2. Create Database `fakenews_detection`

Di Query Tool pgAdmin atau psql console:

```sql
-- Create database
CREATE DATABASE fakenews_detection;

-- Connect to database
\c fakenews_detection
```

### 3. Create Table `feedback`

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

### 4. Update `.env` File

Tambahkan ke `Backend/fastapi-app/.env`:

```env
# Database Configuration
USE_DATABASE=false  # Set false dulu untuk testing
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/fakenews_detection
```

**⚠️ GANTI `YOUR_PASSWORD` dengan password PostgreSQL Anda!**

### 5. Install Dependencies

```powershell
cd Backend/fastapi-app
pip install psycopg2-binary sqlalchemy
```

### 6. Test Koneksi

```powershell
python
```

```python
from app.database import engine
from sqlalchemy import text

# Test connection
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print("✅ Connected to:", result.fetchone())
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

### 7. Migrate Data dari CSV

```powershell
python migrate_to_db.py
```

Expected output:
```
======================================================================
MIGRATING FEEDBACK.CSV TO POSTGRESQL
======================================================================

1️⃣  Creating tables...
   ✅ Tables created successfully

2️⃣  Reading feedback.csv...
   ✅ Found 102 records

3️⃣  Migrating to PostgreSQL...
   ✅ Migrated 102 records successfully

======================================================================
✅ MIGRATION COMPLETED
======================================================================
```

### 8. Enable Database Mode

Update `.env`:
```env
USE_DATABASE=true  # ✅ Enable database
```

Restart FastAPI:
```powershell
# Stop server (Ctrl+C)
uvicorn app.main:app --reload --port 8000
```

### 9. Verify di Admin Dashboard

1. Buka: http://localhost:3001
2. Cek stats dashboard
3. Data harus dari PostgreSQL (bukan CSV)

## Troubleshooting

### Password Authentication Failed
- Verify password PostgreSQL Anda benar
- Update DATABASE_URL di `.env` dengan password yang tepat

### Database Does Not Exist
- Run `CREATE DATABASE fakenews_detection;` di psql/pgAdmin

### Table Does Not Exist  
- Run CREATE TABLE script dari Step 3

### Connection Refused
- Pastikan PostgreSQL service running:
  ```powershell
  Get-Service postgresql-x64-18
  Start-Service postgresql-x64-18  # Jika stopped
  ```

## Next Steps Setelah Database Setup

1. ✅ Database terkoneksi
2. ✅ Data ter-migrate
3. 🔄 Test auto-retrain dengan database backend
4. 📊 Monitor performa query
5. 🚀 Deploy dengan database production-ready

---

**Dokumentasi Lengkap**: Lihat `POSTGRESQL_SETUP.md` dan `QUICK_START_MIGRATION.md`
