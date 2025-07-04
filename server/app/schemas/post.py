from pydantic import BaseModel
from typing import List, Optional

class CommentSchema(BaseModel):
    message: str
    sentiment: str
    created_time: str

class PostWithCommentsSchema(BaseModel):
    id: str
    message: Optional[str]
    created_time: str
    image_url: Optional[str]
    likes: int
    shares: int
    sentiment: str
    comments: List[CommentSchema]

    model_config = {
        "from_attributes": True
    }