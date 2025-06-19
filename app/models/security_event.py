# 无需定义 feedback_id 和 feedback 关系了
from sqlalchemy import Column, String, Integer, BigInteger, TIMESTAMP, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class SecurityEvent(Base):
    __tablename__ = 'security_events'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    house_id = Column(BigInteger, ForeignKey('houses.id'), nullable=False, index=True)
    device_id = Column(BigInteger, ForeignKey('devices.id'), nullable=True, index=True)
    event_type = Column(String(50), nullable=False)
    event_time = Column(TIMESTAMP(timezone=True), nullable=False)
    description = Column(String, nullable=True)
    is_handled = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    house = relationship("House", back_populates="security_events")
    device = relationship("Device", back_populates="security_events")