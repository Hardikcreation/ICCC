from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.facebook import router as facebook_router

app = FastAPI()
app.include_router(facebook_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API is running. Visit /api/docs"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)