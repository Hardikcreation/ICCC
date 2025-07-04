from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.post import Post
from app.db.models.comment import Comment
from app.schemas.post import PostWithCommentsSchema
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/facebook/posts", response_model=List[PostWithCommentsSchema])
def get_facebook_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    data = []
    for post in posts:
        comments = db.query(Comment).filter(Comment.post_id == post.id).all()
        data.append({
            "id": post.id,
            "message": post.message,
            "created_time": post.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "image_url": post.image_url,
            "likes": post.likes,
            "shares": post.shares,
            "sentiment": post.sentiment,
            "comments": [
                {
                    "message": c.message,
                    "sentiment": c.sentiment,
                    "created_time": c.created_time.strftime("%Y-%m-%d %H:%M:%S")
                } for c in comments
            ]
        })
    return data
