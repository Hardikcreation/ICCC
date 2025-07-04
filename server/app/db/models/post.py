from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.session import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(String, primary_key=True, index=True)
    message = Column(String)
    created_time = Column(DateTime)
    image_url = Column(String)
    likes = Column(Integer)
    shares = Column(Integer)
    sentiment = Column(String)
    comments = relationship("Comment", back_populates="post")
