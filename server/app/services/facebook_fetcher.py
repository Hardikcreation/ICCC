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

# Load sentiment model
print("Loading sentiment model...")
model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
print("Device set to use cpu")


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
    except Exception as e:
        print("Sentiment analysis error:", e)
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
    except Exception as e:
        print("Error fetching URL:", e)
        return {}


async def fetch_and_store_data(db: Session):
    print("Fetching posts from Facebook...")

    async with aiohttp.ClientSession() as session:
        def get_posts_url():
            return (
                f"https://graph.facebook.com/v20.0/{PAGE_ID}/posts"
                f"?limit=10&fields=message,created_time,attachments{{media}},"
                f"likes.summary(true),shares&access_token={ACCESS_TOKEN}"
            )

        def get_comments_url(post_id):
            return f"https://graph.facebook.com/v20.0/{post_id}/comments?limit=30&access_token={ACCESS_TOKEN}"

        posts_url = get_posts_url()
        print("Posts URL:", posts_url)

        posts_response = await fetch_url(session, posts_url)
        print("Raw posts response:", posts_response)

        posts = posts_response.get('data', [])
        if not posts:
            print("No posts found in API response")
            return "No posts found"

        comment_tasks = []
        for post in posts:
            post_id = post.get("id")
            print(f"Processing post: {post_id}")
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
                    # page_id=PAGE_ID,
                    message=message,
                    created_time=created_time,
                    image_url=image_url,
                    likes=likes,
                    shares=shares,
                    sentiment=sentiment
                ))
                print(f"Saved post: {post_id}")

            comment_tasks.append(fetch_url(session, get_comments_url(post_id)))

        comment_results = await asyncio.gather(*comment_tasks)

        for post, comment_data in zip(posts, comment_results):
            print(f"Processing comments for post {post['id']}")
            comments = comment_data.get("data", [])
            for comment in comments:
                text = comment.get("message", "")
                created = convert_datetime(comment.get("created_time"))
                if not text:
                    continue

                sentiment = analyze_sentiment(text)
                comment_id = generate_comment_id(post["id"], str(created), text)

                if not db.get(Comment, comment_id):
                    db.add(Comment(
                        id=comment_id,
                        post_id=post["id"],
                        message=text,
                        created_time=created,
                        sentiment=sentiment
                    ))
                    print(f"Saved comment: {comment_id}")

        try:
            db.commit()
            print("Database commit successful")
            return "Facebook data fetched and stored successfully"
        except Exception as e:
            db.rollback()
            print("Database error:", e)
            return "Failed to store Facebook data"


if __name__ == "__main__":
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        result = asyncio.run(fetch_and_store_data(db))
        print(result)
    finally:
        db.close()
