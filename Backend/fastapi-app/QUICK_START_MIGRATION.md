# 🚀 Quick Start: PostgreSQL Migration

Panduan migrasi dari CSV ke PostgreSQL **dalam 10 menit**.

> **Update**: Menggunakan PostgreSQL lokal, bukan Supabase (lebih sederhana untuk data text).

---

## ✅ Pre-Migration Checklist

Before starting, ensure you have:
- [ ] PostgreSQL installed (lihat `POSTGRESQL_SETUP.md` untuk instalasi)
- [ ] Python environment with dependencies installed
- [ ] Database `fakenews_detection` sudah dibuat

---

## 📋 Step-by-Step Migration

### Step 1: Install PostgreSQL (5 min)

**Jika belum install PostgreSQL:**

1. Download dari https://www.postgresql.org/download/windows/
2. Install dengan default settings
3. **Catat password postgres** yang Anda buat saat instalasi
4. Verify service running:
   ```powershell
   Get-Service postgresql*
   # Status: Running
   ```

**Detail lengkap**: Lihat `POSTGRESQL_SETUP.md`

---

### Step 2: Create Database & Table (2 min)

**Opsi A: Menggunakan pgAdmin 4** (GUI - Recommended)

1. Buka pgAdmin 4 dari Start Menu
2. Connect ke PostgreSQL 16 (masukkan password)
3. Right-click "Databases" > Create > Database
   - Name: `fakenews_detection`
   - Owner: `postgres`
   - Save
4. Right-click database > Query Tool
5. Copy-paste SQL ini:

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

-- Create indexes
CREATE INDEX idx_feedback_prediction ON feedback(prediction);
CREATE INDEX idx_feedback_created_at ON feedback(created_at);
```

6. Execute (F5)

**Opsi B: Command Line**

```powershell
cd "C:\Program Files\PostgreSQL\16\bin"
.\psql -U postgres

CREATE DATABASE fakenews_detection;
\c fakenews_detection
# (Paste SQL di atas)
\q
```

---

### Step 3: Configure Environment (1 min)

1. **Navigate to backend**
   ```powershell
   cd Backend/fastapi-app
   ```

2. **Edit `.env`** (atau copy dari `.env.example`):
   ```env
   # Keep existing
   HF_MODEL_REPO=Davidbio/fakenewsdetection-indobert
   HF_TOKEN=your_token_here

   # Add database config
   USE_DATABASE=false
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/fakenews_detection
   ```
   
   **⚠️ Ganti `your_password` dengan password PostgreSQL Anda!**

---

### Step 4: Install Dependencies (2 min)

```powershell
# From Backend/fastapi-app directory
pip install -r requirements.txt
```

Expected output:
```
Installing collected packages: sqlalchemy, psycopg2-binary, alembic
Successfully installed sqlalchemy-2.x.x psycopg2-binary-2.x.x alembic-1.x.x
```

---

### Step 5: Run Migration Script (1 min)

```powershell
# From Backend/fastapi-app directory
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

======================================================================
✅ MIGRATION COMPLETED SUCCESSFULLY!
======================================================================
```

---

### Step 6: Enable Database Mode (30 sec)

1. **Update `.env`**:
   ```env
   USE_DATABASE=true
   ```

2. **Restart FastAPI server**:
   ```powershell
   # Stop current server (Ctrl+C)
   # Restart
   uvicorn app.main:app --reload --port 8000
   ```

3. **Test Admin Dashboard**:
   - Open: http://localhost:3001
   - Verify stats are loading from PostgreSQL
   - Check browser console: No errors

---

## ✅ Verification Checklist

After migration, verify:

- [ ] **pgAdmin 4** (atau psql)
  - Buka pgAdmin 4
  - Navigate: fakenews_detection > Tables > feedback
  - View/Edit Data > All Rows
  - Should see all records from CSV

- [ ] **Admin Dashboard**
  - Stats displayed correctly
  - Total checks = number of records
  - Percentages add up to 100%

- [ ] **Backend Logs**
  - No database connection errors
  - Queries executing successfully

---

## 🔄 Development vs Production

### Development Mode (CSV)
```env
USE_DATABASE=false
```
- Uses `feedback.csv` for local testing
- No database connection needed
- Faster for development

### Production Mode (PostgreSQL)
```env
USE_DATABASE=true
DATABASE_URL=postgresql://...
```
- Uses Supabase PostgreSQL
- Production-ready
- Supports concurrent access

---

## 🐛 Troubleshooting

### Error: "DATABASE_URL not set"
**Solution**: Add `DATABASE_URL` to `.env` file

### Error: "could not connect to server"
**Solutions**:
1. Check PostgreSQL service running:
   ```powershell
   Get-Service postgresql*
   # Jika Stopped, jalankan:
   Start-Service postgresql-x64-16
   ```
2. Verify connection string format
3. Check password correct

### Error: "relation 'feedback' does not exist"
**Solution**: Run CREATE TABLE SQL dari Step 2

### Error: "password authentication failed"
**Solution**: Update DATABASE_URL di `.env` dengan password PostgreSQL yang benar

### Migration shows 0 records
**Solutions**:
1. Check `feedback.csv` exists at: `Model IndoBERT/data/feedback/feedback.csv`
2. Verify CSV has data (not just headers)
3. Check file path in migration script

---

## 📊 PostgreSQL Management Tips

### View Data dengan pgAdmin 4
- **Table Editor** > `feedback` table
- Click rows to view details

### Query Statistics
```sql
-- Total records
SELECT COUNT(*) FROM feedback;

-- Hoax vs Valid
SELECT prediction, COUNT(*) as count
FROM feedback
GROUP BY prediction;

-- Recent entries
SELECT * FROM feedback
ORDER BY created_at DESC
LIMIT 10;
```

### Backup Database
```powershell
# Backup
cd "C:\Program Files\PostgreSQL\16\bin"
.\pg_dump -U postgres -d fakenews_detection -F c -f C:\backup\fakenews.dump

# Restore
.\pg_restore -U postgres -d fakenews_detection C:\backup\fakenews.dump
```

---

## 🎯 Next Steps

After successful migration:

1. **Test New Predictions**
   - Submit text via user app (port 3000)
   - Check if saved to database
   - Verify admin stats update

2. **Backup Strategy**
   - Weekly backup dengan `pg_dump`
   - Save ke external drive/cloud storage
   - Optional: Export ke CSV untuk archive

3. **Monitor Usage**
   - Check database size: `SELECT pg_size_pretty(pg_database_size('fakenews_detection'));`
   - PostgreSQL lokal: no storage limits (tergantung disk space)

4. **Production Deployment**
   - Update production `.env` dengan `USE_DATABASE=true`
   - Keep development as `USE_DATABASE=false`

---

## 📚 Additional Resources

- **PostgreSQL Setup Guide**: `POSTGRESQL_SETUP.md` (lengkap dengan instalasi)
- **Database Models**: `app/models.py`
- **API Documentation**: http://localhost:8000/docs
- **pgAdmin 4 Docs**: https://www.pgadmin.org/docs/

---

**Need help?** Check `POSTGRESQL_SETUP.md` for detailed troubleshooting.
