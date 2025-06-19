# app/models/device.py

from sqlalchemy import Column, String, Integer, BigInteger, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Device(Base):
    __tablename__ = 'devices'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    house_id = Column(BigInteger, ForeignKey('houses.id'), nullable=False, index=True)
    device_name = Column(String(100), nullable=False)
    device_type = Column(String(50), nullable=False)
    location = Column(String(50), nullable=True)
    model = Column(String(100), nullable=True)
    added_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系：设备属于某个房屋
    house = relationship("House", back_populates="devices")
    # 该设备产生的使用记录
    usage_records = relationship("UsageRecord", back_populates="device")
    # 该设备可能产生的安防事件
    security_events = relationship("SecurityEvent", back_populates="device")
