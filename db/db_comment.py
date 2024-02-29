from fastapi import HTTPException, status
from routers.schemas import CommentBase
from sqlalchemy.orm.session import Session
from db.models import DbComment
from datetime import datetime

def create(db: Session, request: CommentBase):
    new_comment = DbComment(
        text=request.text,
        username=request.username,
        post_id=request.post_id,
        timestamp=datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return "ok"


def get_all(db: Session, post_id: int):
    return db.query(DbComment).filter(DbComment.id == post_id)


