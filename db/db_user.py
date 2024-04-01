from db.models import DbUser, Follow, DbPost
from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.hashing import Hash
from fastapi import HTTPException, status

def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        bio=request.bio,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username {username} not found")
    return user

def get_user_posts(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username {username} not found")
    posts = db.query(DbPost).filter(DbPost.user_id == user.id).all()
    return posts


def get_all(db: Session):
  return db.query(DbUser).all()


def follow_user(db: Session, follower_username: str, followed_username: str):
    follower = db.query(DbUser).filter(DbUser.username == follower_username).first()
    followed = db.query(DbUser).filter(DbUser.username == followed_username).first()
    if not follower or not followed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    follower.following.append(followed)
    db.commit()
    return follower


def unfollow_user(db: Session, follower_username: str, followed_username: str):
    follower = db.query(DbUser).filter(DbUser.username == follower_username).first()
    followed = db.query(DbUser).filter(DbUser.username == followed_username).first()

    if not follower or not followed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if the follower is already following the followed user
    follow_record = db.query(Follow).filter(Follow.follower_id == follower.id,
                                            Follow.followed_id == followed.id).first()

    if not follow_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not following")

    # Remove the follow record
    db.delete(follow_record)
    db.commit()

    return {"detail": "Unfollowed successfully"}

