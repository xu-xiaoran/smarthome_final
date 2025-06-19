from sqlalchemy import Column, String, BigInteger, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    full_name = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    user_type = Column(String(20), nullable=False, server_default='regular')

    houses = relationship("House", back_populates="owner")
    usage_records = relationship("UsageRecord", back_populates="user")
    feedbacks = relationship("UserFeedback", back_populates="user")
