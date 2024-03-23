from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_like
from routers.schemas import LikeBase, LikeDisplay, UserAuth
from auth.oauth2 import get_current_user


router = APIRouter(prefix='/like', tags=['like'])

@router.get('/all/{post_id}')
def likes(post_id: int, db: Session = Depends(get_db)):
    return db_like.get_all(db, post_id)

@router.post('/like/{post_id}')
def like(post_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_like.create(db, post_id, current_user.id)

@router.post('/unlike/{post_id}')
def unlike(post_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_like.delete(db, post_id, current_user.id)