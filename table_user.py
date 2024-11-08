from database import Base, SessionLocal
from sqlalchemy import Integer, String, Column, func

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)

session = SessionLocal()

if __name__ == "__main__":
    print([user for user in session.query(User.country, User.os, func.count('*')).filter(User.exp_group == 3).group_by(User.country, User.os).having(func.count('*') > 100).order_by(func.count('*').desc()).all()])