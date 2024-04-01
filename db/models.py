from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Follow(Base):
    __tablename__ = "follows"
    follower_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    followed_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

class DbUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    bio = Column(String, nullable=True)
    items = relationship('DbPost', back_populates='user')
    followers = relationship(
        "DbUser",
        secondary="follows",
        primaryjoin=id == Follow.followed_id,
        secondaryjoin=id == Follow.follower_id,
        back_populates="following",
    )
    following = relationship(
        "DbUser",
        secondary="follows",
        primaryjoin=id == Follow.follower_id,
        secondaryjoin=id == Follow.followed_id,
        back_populates="followers",
    )


class DbPost(Base):
  __tablename__ = 'post'
  id = Column(Integer, primary_key=True, index=True)
  image_url = Column(String)
  image_url_type = Column(String)
  caption = Column(String)
  timestamp = Column(DateTime)
  user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship('DbUser', back_populates='items')
  comments = relationship("DbComment", back_populates='post')
  likes = relationship("DbLike", back_populates="post")


class DbComment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("DbPost", back_populates='comments')


class DbLike(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("DbPost", back_populates="likes")
