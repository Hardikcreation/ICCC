from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.post import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String, ForeignKey("posts.id"))
    message = Column(String)
    sentiment = Column(String)
    created_time = Column(DateTime)
    post = relationship("Post", back_populates="comments")