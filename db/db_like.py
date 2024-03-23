from fastapi import HTTPException, status
from routers.schemas import LikeBase
from sqlalchemy.orm.session import Session
from db.models import DbLike
from datetime import datetime

def create(db: Session, post_id: int, user_id: int):
    new_like = DbLike(
        user_id=user_id,
        post_id=post_id,
    )
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like

def delete(db: Session, post_id: int, user_id: int):
    like = db.query(DbLike).filter(DbLike.post_id == post_id, DbLike.user_id == user_id).first()
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Like for post {post_id} by user {user_id} not found")
    db.delete(like)
    db.commit()
    return "ok"


def get_all(db: Session, post_id: int):
  return db.query(DbLike).filter(DbLike.post_id == post_id).all()