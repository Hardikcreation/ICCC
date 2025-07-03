# backend/app/schemas/facebook.py
from pydantic import BaseModel
from datetime import datetime

class FacebookPostCreate(BaseModel):
    message: str
    created_time: datetime
    sentiment: str

class FacebookPostResponse(FacebookPostCreate):
    id: str
