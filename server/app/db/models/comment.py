from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.session import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(String, primary_key=True)
    post_id = Column(String, ForeignKey("posts.id"))
    message = Column(String)
    created_time = Column(DateTime)
    sentiment = Column(String)
