#!/usr/bin/env python3
"""
Database Migration Script - Creates tables from SQLAlchemy models
Run this script to initialize the database schema
"""

import os
import sys
from pathlib import Path

# Add app directory to path for imports
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from app.database import Base, engine
from app.models import (
    DetectionResult,
    UserFeedback,
    ModelMetadata,
    AdminUser,
    ApiKey
)

def create_tables():
    """Create all tables defined in models.py"""
    try:
        print("🔧 Starting database migration...")
        print(f"📊 Database URL: {os.getenv('DATABASE_URL', 'NOT SET')[:50]}...")
        
        # Create all tables
        print("📦 Creating tables from SQLAlchemy models...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database migration completed successfully!")
        print(f"📋 Tables created: {', '.join([table.name for table in Base.metadata.sorted_tables])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_tables()
    sys.exit(0 if success else 1)
