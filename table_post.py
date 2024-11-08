from database import Base, SessionLocal
from sqlalchemy import Integer, String, Column

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)

session = SessionLocal()

if __name__ == "__main__":
    print([post.id for post in session.query(Post).filter(Post.topic == "business").order_by(Post.id.desc()).limit(10)])