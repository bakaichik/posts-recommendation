from table_user import User
from table_post import Post
from table_feed import Feed
from schema import PostGet, UserGet, FeedGet
from database import SessionLocal
from fastapi import FastAPI, HTTPException, Depends
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db

@app.get("/user/{id}", response_model=UserGet)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(User).filter(User.id == id).limit(1).first()

    logger.debug(f"User: {result}")

    if result is None:
        raise HTTPException(status_code=404, detail="user not found")

    return UserGet(**result.__dict__)

@app.get("/post/{id}", response_model=PostGet)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Post).filter(Post.id == id).limit(1).first()

    logger.debug(f"Result: {result}")

    if result is None:
        raise HTTPException(status_code=404, detail="post not found")

    return PostGet(**result.__dict__)


@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_user_feed_by_id(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.user_id == id).order_by(Feed.time.desc()).limit(limit).all()

    logger.debug(f"Feed user: {result}")

    if result is None:
        raise []

    return result

@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_post_feed_by_id(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.post_id == id).order_by(Feed.time.desc()).limit(limit).all()

    logger.debug(f"Feed post: {result}")

    if result is None:
        return []

    return result


@app.get("/post/recommendations/", response_model=List[PostGet])
def get_post_top_recommendations_by_id(limit: int = 10, db: Session = Depends(get_db)):
    top_posts = (
        db.query(Post)
        .join(Feed, Post.id == Feed.post_id)
        .filter(Feed.action == 'like')
        .group_by(Post.id)
        .order_by(func.count(Feed.post_id).desc())
        .limit(limit)
        .all()
    )

    # Log the results directly
    logger.debug(f"Post recommendations: {top_posts}")

    return top_posts if top_posts else []