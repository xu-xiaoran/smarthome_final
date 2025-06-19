# app/models/usage_record.py

from sqlalchemy import Column, String, Integer, BigInteger, TIMESTAMP, ForeignKey, Interval, func
from sqlalchemy.orm import relationship
from app.database import Base

class UsageRecord(Base):
    __tablename__ = 'usage_records'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    device_id = Column(BigInteger, ForeignKey('devices.id'), nullable=False, index=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, index=True)
    action = Column(String(50), nullable=False)  # 如 turn_on, turn_off, set_temp 等
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=True)
    usage_duration = Column(Interval, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    device = relationship("Device", back_populates="usage_records")
    user = relationship("User", back_populates="usage_records")
