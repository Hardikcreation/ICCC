# ✅ server/fetch_facebook_data.py
from app.services.facebook_fetcher import fetch_and_store_data
from app.db.session import SessionLocal
import asyncio

if __name__ == "__main__":
    db = SessionLocal()
    try:
        asyncio.run(fetch_and_store_data(db))
        print("✅ Facebook data fetched and stored successfully")
    finally:
        db.close()
