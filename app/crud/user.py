# app/crud/user.py

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from typing import Optional
from passlib.context import CryptContext

# 用 passlib 来做密码哈希，安全地存储用户密码
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    # 接收到明文密码，需要先哈希
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        password_hash=hashed_password,
        email=user.email,
        phone=user.phone,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # 刷新模型，以便拿到数据库分配的 id 等字段
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    user_obj = db.query(User).filter(User.id == user_id).first()
    if not user_obj:
        return False
    db.delete(user_obj)
    db.commit()
    return True

def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
    """
    支持更新字段：email, phone, full_name, user_type 等，
    这里传入的 kwargs 键必须与 User 模型字段相同。
    """
    user_obj = db.query(User).filter(User.id == user_id).first()
    if not user_obj:
        return None
    for key, value in kwargs.items():
        setattr(user_obj, key, value)
    db.commit()
    db.refresh(user_obj)
    return user_obj

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    验证用户名/密码是否匹配，用于登录逻辑。
    """
    user_obj = get_user_by_username(db, username)
    if not user_obj:
        return None
    if not verify_password(password, user_obj.password_hash):
        return None
    return user_obj

from typing import List

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()
from typing import List

def create_users(db: Session, users: List[UserCreate]) -> List[User]:
    db_users = []
    for user in users:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            password_hash=hashed_password,
            email=user.email,
            phone=user.phone,
            full_name=user.full_name
        )
        db_users.append(db_user)
        db.add(db_user)
    db.commit()
    for user in db_users:
        db.refresh(user)
    return db_users
