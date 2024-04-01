from fastapi import APIRouter
from sqlalchemy.orm.session import Session

from auth.oauth2 import get_current_user
from typing import List

from routers.schemas import UserBase, UserDisplay, UserAuth, PostBase, PostDisplay
from fastapi.param_functions import Depends
from db.database import get_db
from db import db_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


@router.get('/all', response_model=List[UserDisplay])
def users(db: Session = Depends(get_db)):
    return db_user.get_all(db)

@router.get('/{username}', response_model=UserDisplay)
def user_info(username: str, db: Session = Depends(get_db)):
    return db_user.get_user_by_username(db, username)


@router.get('/{username}/posts', response_model=List[PostDisplay])
def user_posts(username: str, db: Session = Depends(get_db)):
    return db_user.get_user_posts(db, username)

@router.post('/follow/{username}')
def follow(username: str, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_user.follow_user(db, current_user.username, username)


@router.post('/unfollow/{username}')
def unfollow(username: str, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_user.unfollow_user(db, current_user.username, username)
