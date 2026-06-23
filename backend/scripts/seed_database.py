# ==============================================================
# RetailPulse Server – Database Seeder (CSV → PostgreSQL)
# ==============================================================
# Usage: python -m scripts.seed_database
# ==============================================================

import os
import sys
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.models import User, Transaction, CustomerSegment, Forecast, ChurnRecord
from app.utils.security import hash_password


def seed():
    print("=" * 60)
    print("  RetailPulse Database Seeder")
    print("=" * 60)

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")

    db = SessionLocal()

    try:
        # ── Seed Admin User ─────────────────────────────────
        if db.query(User).count() == 0:
            admin = User(
                email="admin@retailpulse.com",
                hashed_password=hash_password("admin123"),
                full_name="Admin User",
                role="admin",
            )
            analyst = User(
                email="analyst@retailpulse.com",
                hashed_password=hash_password("analyst123"),
                full_name="Analyst User",
                role="analyst",
            )
            db.add_all([admin, analyst])
            db.commit()
            print("✅ Default users seeded (admin@retailpulse.com / admin123)")
        else:
            print("⏭️  Users already exist, skipping")

        # ── Seed Transactions ───────────────────────────────
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")

        if db.query(Transaction).count() == 0:
            path = os.path.join(data_dir, "clean_retail_data.csv")
            if os.path.exists(path):
                print("Loading transactions (this may take a minute)...")
                df = pd.read_csv(path, parse_dates=["InvoiceDate"])
                # Map CSV columns to ORM column names exactly
                df = df.rename(columns={
                    "Invoice": "invoice",
                    "StockCode": "stock_code",
                    "Description": "description",
                    "Quantity": "quantity",
                    "InvoiceDate": "invoice_date",
                    "Price": "price",
                    "Customer ID": "customer_id",
                    "Country": "country",
                    "Revenue": "revenue",
                })
                df.to_sql("transactions", engine, if_exists="append", index=False, chunksize=5000)
                print(f"Transactions seeded: {len(df):,} rows")
        else:
            print("⏭️  Transactions already exist, skipping")

        # ── Seed Segments ───────────────────────────────────
        if db.query(CustomerSegment).count() == 0:
            path = os.path.join(data_dir, "customer_segments.csv")
            if os.path.exists(path):
                df = pd.read_csv(path)
                df.columns = [c.lower().replace(" ", "_") for c in df.columns]
                df.to_sql("customer_segments", engine, if_exists="append", index=False)
                print(f"✅ Segments seeded: {len(df):,} rows")
        else:
            print("⏭️  Segments already exist, skipping")

        # ── Seed Forecast ───────────────────────────────────
        if db.query(Forecast).count() == 0:
            path = os.path.join(data_dir, "sales_forecast.csv")
            if os.path.exists(path):
                df = pd.read_csv(path, parse_dates=["ds"])
                df.to_sql("forecasts", engine, if_exists="append", index=False)
                print(f"✅ Forecast seeded: {len(df):,} rows")
        else:
            print("⏭️  Forecast already exist, skipping")

        # ── Seed Churn ──────────────────────────────────────
        if db.query(ChurnRecord).count() == 0:
            path = os.path.join(data_dir, "churn_data.csv")
            if os.path.exists(path):
                df = pd.read_csv(path)
                df.columns = [c.lower().replace(" ", "_") for c in df.columns]
                df.to_sql("churn_records", engine, if_exists="append", index=False)
                print(f"✅ Churn records seeded: {len(df):,} rows")
        else:
            print("⏭️  Churn records already exist, skipping")

    finally:
        db.close()

    print("\n✅ Database seeding complete!")


if __name__ == "__main__":
    seed()
