# app/models/house.py

from sqlalchemy import Column, String, Integer, BigInteger, Numeric, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class House(Base):
    __tablename__ = 'houses'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, index=True)
    address = Column(String(200), nullable=True)
    area_sqm = Column(Numeric(8, 2), nullable=False)
    room_count = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系：房屋属于某个用户
    owner = relationship("User", back_populates="houses")
    # 一个房屋可以有多个设备
    devices = relationship("Device", back_populates="house")
    # 一个房屋可以有多条安防事件
    security_events = relationship("SecurityEvent", back_populates="house")
