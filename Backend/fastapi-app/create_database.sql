-- SQL Script untuk membuat database dan table fakenews_detection
-- Jalankan di pgAdmin 4 Query Tool

-- Step 1: Create database (run di default 'postgres' database)
CREATE DATABASE fakenews_detection;

-- Step 2: Setelah database dibuat, connect ke database 'fakenews_detection'
-- Lalu jalankan script di bawah ini:

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

-- Verify tables created
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Expected output:
-- table_name
-- ------------
-- feedback
-- feedback_stats
