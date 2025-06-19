from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# 修正导入方式
from app.schemas.user import User, UserCreate
from app import crud
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.user.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    db_user = crud.user.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    return crud.user.create_user(db, user)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户未找到")
    return db_user

@router.get("/", response_model=List[User])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.user.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.user.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        hashed = crud.user.get_password_hash(update_data.pop("password"))
        update_data["password_hash"] = hashed
    return crud.user.update_user(db, user_id, **update_data)

