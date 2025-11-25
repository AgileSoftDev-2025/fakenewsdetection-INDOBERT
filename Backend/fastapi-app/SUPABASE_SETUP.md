# Supabase PostgreSQL Setup Guide

## 1. Create Supabase Account

1. Go to https://supabase.com
2. Sign up with GitHub
3. Create new project:
   - Project name: `fakenews-detection`
   - Database password: (save this!)
   - Region: Southeast Asia (Singapore) - closest to Indonesia

## 2. Get Database URL

After project is created:
1. Go to Project Settings → Database
2. Copy **Connection string** → **URI**
3. Format: `postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`

## 3. Create Tables

Go to SQL Editor in Supabase Dashboard and run:

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
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_feedback_prediction ON feedback(prediction);
CREATE INDEX idx_feedback_timestamp ON feedback(timestamp);
CREATE INDEX idx_feedback_created_at ON feedback(created_at);

-- Create view for statistics (optional but helpful)
CREATE VIEW feedback_stats AS
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as hoax,
    SUM(CASE WHEN prediction = 0 THEN 1 ELSE 0 END) as valid,
    ROUND(SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100, 1) as hoax_percentage,
    ROUND(SUM(CASE WHEN prediction = 0 THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100, 1) as valid_percentage
FROM feedback;
```

## 4. Enable Row Level Security (RLS) - Optional

For production security:

```sql
-- Enable RLS
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can read
CREATE POLICY "Allow public read access" ON feedback
    FOR SELECT USING (true);

-- Policy: Service role can insert/update
CREATE POLICY "Allow service role write access" ON feedback
    FOR ALL USING (
        auth.jwt() ->> 'role' = 'service_role'
    );
```

## 5. Environment Variables

Add to `Backend/fastapi-app/.env`:

```env
# Supabase Database
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
USE_DATABASE=true

# Keep existing
HF_MODEL_REPO=Davidbio/fakenewsdetection-indobert
HF_TOKEN=your_huggingface_token_here
```

## 6. Test Connection

Use Supabase SQL Editor or any PostgreSQL client to verify connection.

## Free Tier Limits

Supabase free tier includes:
- ✅ 500 MB database space
- ✅ Unlimited API requests
- ✅ 50,000 monthly active users
- ✅ 2 GB bandwidth
- ✅ Auto backups (7 days retention)

Perfect for this project! 🎉
