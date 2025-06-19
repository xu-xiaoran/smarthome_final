# app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# 1. 用户创建时（Request Body）
class UserCreate(BaseModel):
    username: str
    password: str     # 这里存的是明文密码，后面在后端会做哈希才入库
    email: EmailStr
    phone: Optional[str] = None
    full_name: Optional[str] = None

# 2. 用户展示时（Response）
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: Optional[str] = None
    full_name: Optional[str] = None
    created_at: datetime
    user_type: str

    class Config:
        orm_mode = True    # 告诉 Pydantic 可以从 ORM 对象（SQLAlchemy model）中读取数据
