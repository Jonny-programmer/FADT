from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime, date
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    birth_date = Column(DateTime, nullable=True)
    blogs = relationship('Blog', back_populates='author')
    items = relationship("Item", back_populates="owner")
    posts = relationship('Post', back_populates='author')
    skeds = relationship('Sked', back_populates='creator')
    videos = relationship('Video', back_populates='creator')
    photoalbums = relationship('Video', back_populates='creator')



class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")

# class AdultUser(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, unique=True)
#
#     name = Column(String, nullable=False)
#     surname = Column(String, nullable=False)
#     patronymic = Column(String, nullable=True)
#
#     nickname = Column(String, nullable=False, unique=True, index=True, default=f"user_{uuid.uuid1()}")
#
#     last_seen = Column(DateTime, default=datetime.now)
#     birth_date = Column(DateTime, nullable=False)
#
#     email = Column(String, nullable=False)
#
#     profile_pic = Column(String, nullable=True)
#     hashed_password = Column(String, nullable=True)
#
#     def set_password(self, password):
#         self.hashed_password = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.hashed_password, password)


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    datetime_created = Column(DateTime, default=datetime.now())
    title = Column(String, nullable=False)
    type = Column(String, nullable=False, default='usual')
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="blogs")
    photo_source = Column(String, nullable=False)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    datetime_created = Column(DateTime, default=datetime.now())
    title = Column(String, nullable=False)
    text = Column(Text, nullable=True)
    photo_source = Column(String, nullable=False)
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    blog = relationship("Blog", back_populates="posts")
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")


class Sked(Base):
    __tablename__ = 'skeds'
    id = Column(Integer, primary_key=True, index=True)
    datetime_created = Column(DateTime, default=datetime.now())
    date = Column(Date, default=date.today())
    file_source = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="skeds")


class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, index=True)
    video_source = Column(String, nullable=False)
    label = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="videos")


class PhotoAlbum(Base):
    __tablename__ = 'photoalbums'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="photoalbums")
    photos = relationship('Photo', back_populates='photoalbum')


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=True)
    photo_source = Column(String, nullable=False)
    photoalbum_id = Column(Integer, ForeignKey('photoalbums.id'))
    photoalbum = relationship('PhotoAlbum', back_populates='photos')

