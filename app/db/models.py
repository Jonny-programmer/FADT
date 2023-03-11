import uuid
from datetime import datetime
from enum import unique
from hashlib import md5

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, VARCHAR, Table
from sqlalchemy.orm import relation as relationship
from werkzeug.security import generate_password_hash, check_password_hash

from .database import Base


class AdultUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True)

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)

    nickname = Column(String, nullable=False, unique=True, index=True, default=f"user_{uuid.uuid1()}")

    last_seen = Column(DateTime, default=datetime.now)
    birth_date = Column(DateTime, nullable=False)

    email = Column(String, nullable=False)

    profile_pic = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    item = Column(String, nullable=True)
    pass
# class Post(Base):
#     __tablename__ = "posts"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("people.id"))
#     owner = relationship("AdultUser", back_populates="nickname")
