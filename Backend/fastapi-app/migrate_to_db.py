"""
Migration script: CSV → PostgreSQL (Supabase)

This script migrates data from feedback.csv to PostgreSQL database.

Usage:
    python migrate_to_db.py

Requirements:
    - Set DATABASE_URL in .env file
    - feedback.csv must exist in Model IndoBERT/data/feedback/
"""

import sys
import csv
from pathlib import Path
from dotenv import load_dotenv
import os

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import engine, Base, SessionLocal
from app.models import Feedback

# Load environment variables
load_dotenv()

# Get repository root (2 levels up from this script)
REPO_ROOT = Path(__file__).resolve().parents[2]


def migrate_csv_to_database():
    """
    Migrate feedback.csv data to PostgreSQL database
    """
    # Check DATABASE_URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ ERROR: DATABASE_URL not set in .env file")
        print("Please add your Supabase PostgreSQL URL to .env")
        return False

    print("=" * 70)
    print("MIGRATING FEEDBACK.CSV TO POSTGRESQL")
    print("=" * 70)
    print(
        f"\n📊 Database: {database_url.split('@')[1] if '@' in database_url else 'configured'}\n"
    )

    # Create tables
    print("1️⃣  Creating tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("   ✅ Tables created successfully")
    except Exception as e:
        print(f"   ❌ Error creating tables: {e}")
        return False

    # Find feedback.csv
    csv_path = REPO_ROOT / "Model IndoBERT" / "data" / "feedback" / "feedback.csv"

    if not csv_path.exists():
        print(f"   ❌ feedback.csv not found at: {csv_path}")
        return False

    print(f"   ✅ Found CSV: {csv_path}")

    # Read CSV and migrate
    print("\n2️⃣  Reading CSV data...")
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_count = db.query(Feedback).count()
        if existing_count > 0:
            print(f"   ⚠️  Database already has {existing_count} records")
            response = input("   Do you want to clear and re-import? (yes/no): ")
            if response.lower() == "yes":
                db.query(Feedback).delete()
                db.commit()
                print("   ✅ Existing data cleared")
            else:
                print("   ℹ️  Migration cancelled")
                return False

        # Read CSV
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        print(f"   ✅ Read {len(rows)} records from CSV")

        # Insert into database
        print("\n3️⃣  Inserting records into database...")
        inserted = 0
        errors = 0

        for i, row in enumerate(rows, 1):
            try:
                feedback = Feedback(
                    timestamp=int(row["timestamp"]) if row.get("timestamp") else None,
                    model_name=row.get("model_name"),
                    model_version=row.get("model_version"),
                    text_length=int(row["text_length"])
                    if row.get("text_length")
                    else None,
                    prediction=int(row["prediction"])
                    if row.get("prediction")
                    else None,
                    prob_hoax=float(row["prob_hoax"]) if row.get("prob_hoax") else None,
                    confidence=float(row["confidence"])
                    if row.get("confidence")
                    else None,
                    user_label=int(row["user_label"])
                    if row.get("user_label") and row["user_label"] != ""
                    else None,
                    agreement=row.get("agreement"),
                    raw_text=row.get("raw_text"),
                )
                db.add(feedback)
                inserted += 1

                # Commit in batches of 100
                if i % 100 == 0:
                    db.commit()
                    print(f"   📝 Inserted {i}/{len(rows)} records...")

            except Exception as e:
                errors += 1
                print(f"   ⚠️  Error on row {i}: {e}")
                continue

        # Final commit
        db.commit()

        print(f"\n   ✅ Successfully inserted {inserted} records")
        if errors > 0:
            print(f"   ⚠️  {errors} errors occurred")

        # Verify migration
        print("\n4️⃣  Verifying migration...")
        total = db.query(Feedback).count()
        hoax = db.query(Feedback).filter(Feedback.prediction == 1).count()
        valid = db.query(Feedback).filter(Feedback.prediction == 0).count()

        print(f"   ✅ Total records in database: {total}")
        print(f"   ✅ Hoax: {hoax}")
        print(f"   ✅ Valid: {valid}")

        print("\n" + "=" * 70)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Set USE_DATABASE=true in .env")
        print("2. Restart your FastAPI server")
        print("3. Admin dashboard will now use PostgreSQL")
        print()

        return True

    except Exception as e:
        db.rollback()
        print(f"\n❌ Migration failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        db.close()


if __name__ == "__main__":
    success = migrate_csv_to_database()
    sys.exit(0 if success else 1)
