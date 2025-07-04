import os
import aiohttp
import asyncio
import hashlib
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from transformers import AutoModelForSequenceClassification, XLMRobertaTokenizer, pipeline

from app.db.models.post import Post
from app.db.models.comment import Comment

load_dotenv()

PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def analyze_sentiment(text):
    if not text:
        return "Neutral"
    try:
        result = sentiment_pipeline(text[:512])[0]
        label = result['label'].lower()
        if 'positive' in label:
            return 'Positive'
        elif 'negative' in label:
            return 'Negative'
        return 'Neutral'
    except:
        return "Neutral"

def convert_datetime(dt_str):
    try:
        dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S%z')
        return dt.replace(tzinfo=None)
    except:
        return datetime.utcnow()

def generate_comment_id(post_id, created_time, message):
    data = f"{post_id}_{created_time}_{message}"
    return hashlib.md5(data.encode()).hexdigest()

async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            return await response.json()
    except:
        return {}

async def fetch_and_store_data(db: Session):
    async with aiohttp.ClientSession() as session:
        def get_posts_url():
            return f"https://graph.facebook.com/v20.0/{PAGE_ID}/posts?limit=10&fields=message,created_time,attachments{{media}},likes.summary(true),shares&access_token={ACCESS_TOKEN}"

        def get_comments_url(post_id):
            return f"https://graph.facebook.com/v20.0/{post_id}/comments?limit=30&access_token={ACCESS_TOKEN}"

        posts_url = get_posts_url()
        posts_response = await fetch_url(session, posts_url)
        posts = posts_response.get('data', [])

        if not posts:
            return "No posts found"

        comment_tasks = []
        for post in posts:
            post_id = post.get("id")
            message = post.get("message", "")
            created_time = convert_datetime(post.get("created_time"))
            image_url = ""
            likes = post.get("likes", {}).get("summary", {}).get("total_count", 0)
            shares = post.get("shares", {}).get("count", 0)

            attachments = post.get("attachments", {}).get("data", [])
            if attachments and 'media' in attachments[0]:
                image_url = attachments[0]['media'].get('image', {}).get('src', "")

            sentiment = analyze_sentiment(message)

            if not db.get(Post, post_id):
                db.add(Post(
                    id=post_id,
                    page_id=PAGE_ID,
                    message=message,
                    created_time=created_time,
                    image_url=image_url,
                    likes=likes,
                    shares=shares,
                    sentiment=sentiment
                ))

            comment_tasks.append(fetch_url(session, get_comments_url(post_id)))

        comment_results = await asyncio.gather(*comment_tasks)

        for post, comment_data in zip(posts, comment_results):
            post_id = post["id"]
            comments = comment_data.get("data", [])

            for comment in comments:
                text = comment.get("message", "")
                created = convert_datetime(comment.get("created_time"))
                if not text:
                    continue

                sentiment = analyze_sentiment(text)
                comment_id = generate_comment_id(post_id, str(created), text)

                if not db.get(Comment, comment_id):
                    db.add(Comment(
                        id=comment_id,
                        post_id=post_id,
                        message=text,
                        created_time=created,
                        sentiment=sentiment
                    ))

        try:
            db.commit()
            return "Facebook data fetched and stored successfully"
        except:
            db.rollback()
            return "Failed to store Facebook data"