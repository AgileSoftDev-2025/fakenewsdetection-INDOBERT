#!/usr/bin/env python3
"""
Database Migration Script - Creates tables from SQLAlchemy models
Run this script to initialize the database schema
"""

import os
import sys
import time
from pathlib import Path

# Add app directory to path for imports
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from app.database import Base, engine
from app.models import Feedback  # Import all models here


def create_tables(max_retries=5, retry_delay=3):
    """Create all tables defined in models.py with retry logic"""
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"🔧 Starting database migration (attempt {attempt}/{max_retries})...")
            print(f"📊 Database URL: {os.getenv('DATABASE_URL', 'NOT SET')[:50]}...")

            # Test connection first
            print("🔌 Testing database connection...")
            with engine.connect() as conn:
                print("✅ Database connection successful!")

            # Create all tables
            print("📦 Creating tables from SQLAlchemy models...")
            Base.metadata.create_all(bind=engine)

            print("✅ Database migration completed successfully!")
            print(
                f"📋 Tables created: {', '.join([table.name for table in Base.metadata.sorted_tables])}"
            )

            return True

        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            
            if attempt < max_retries:
                print(f"⏳ Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
            else:
                print("❌ All retry attempts failed!")
                import traceback
                traceback.print_exc()
                return False

    return False


if __name__ == "__main__":
    success = create_tables()
    sys.exit(0 if success else 1)
