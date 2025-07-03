# app/main.py

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from app.api.facebook import router
from app.db.session import Base, engine
from app.db.models import post, comment  # Ensure models are imported so tables get created

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(router, prefix="/api")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "API is running. Visit /api/docs for Swagger UI."}
