# app/api/facebook.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.facebook import fetch_and_store_data

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/fetch-facebook")
async def fetch_facebook(db: Session = Depends(get_db)):
    result = await fetch_and_store_data(db)
    return {"status": result}
