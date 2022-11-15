import uuid
from datetime import datetime
from enum import unique
from hashlib import md5

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, VARCHAR, Table
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from .database import Base


class AdultUser(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, unique=True)

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)

    nickname = Column(String, nullable=False, unique=True, index=True, default=f"user_{uuid.uuid1()}")

    last_seen = Column(DateTime, default=datetime.now)
    birth_date = Column(DateTime, nullable=False)

    # parent_id = Column(Integer, nullable=True)
    # child_id = Column(Integer, nullable=True)

    role = Column(Integer, nullable=False)

    profile_pic = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role_id = relationship("AdultUser", back_populates="role")
    role_name = Column(String, nullable=False)
    # [Admin, Teacher, Parent, Student]


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade_num = Column(Integer, nullable=False)
    grade_letter = Column(VARCHAR(1), nullable=False)

    first_main_teacher = relationship("AdultUser", back_populates="id")
    second_main_teacher = relationship("AdultUser", back_populates="id")


parent_to_child_association = Table('parent_to_child', Base.metadata,
                                    Column('parent_nickname', String, ForeignKey('people.nickname')),
                                    Column('child_nickname', String, ForeignKey('people.nickname')))
grade_to_child_association = Table('grade_to_child', Base.metadata,
                                   Column('grade_id', Integer, ForeignKey('grades.id')),
                                   Column('child_id', Integer, ForeignKey('people.id')))


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
