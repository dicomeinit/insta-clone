from pydantic import BaseModel
from datetime import datetime
from typing import List

# User
class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    username: str
    email: str
    class Config():
        orm_model = True

# Post
class PostBase(BaseModel):
  image_url: str
  image_url_type: str
  caption: str
  creator_id: int

# For PostDisplay
class User(BaseModel):
  username: str
  class Config():
    orm_mode = True

# For PostDisplay
class Comment(BaseModel):
    text: str
    username: str
    timestamp: datetime

    class Config():
        orm_mode = True

class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: User
    comments: List[Comment]
    class Config():
        orm_model = True

class UserAuth(BaseModel):
    id: int
    username: str
    email: str

class CommentBase(BaseModel):
    username: str
    text: str
    post_id: int


class LikeBase(BaseModel):
    post_id: int
    user_id: int

class LikeDisplay(BaseModel):
    id: int
    user_id: int
    post_id: int

    class Config:
        orm_mode = True
