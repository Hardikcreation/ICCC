
from sqlalchemy import Column, String, DateTime, Integer
from app.db.session import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(String, primary_key=True)
    page_id = Column(String)
    message = Column(String)
    created_time = Column(DateTime)
    image_url = Column(String)
    likes = Column(Integer)
    shares = Column(Integer)
    sentiment = Column(String)
