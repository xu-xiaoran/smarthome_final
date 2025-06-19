from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    house_id = Column(Integer, ForeignKey("house_info.id"))

    house = relationship("HouseInfo", back_populates="residents")
    devices = relationship("Device", back_populates="owner")
    feedbacks = relationship("Feedback", back_populates="user")
    usage = relationship("DeviceUsage", back_populates="user")


class HouseInfo(Base):
    __tablename__ = "house_info"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    area = Column(Float)

    residents = relationship("User", back_populates="house")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)  # ✅ 添加主键，避免建表失败
    house_id = Column(Integer)
    device_name = Column(String)
    device_type = Column(String)
    location = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    model = Column(String)

    owner = relationship("User", back_populates="devices")
    usage = relationship("DeviceUsage", back_populates="device")


class DeviceUsage(Base):
    __tablename__ = "device_usage"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)

    device = relationship("Device", back_populates="usage")
    user = relationship("User", back_populates="usage")


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)  # ✅ 添加主键
    house_id = Column(Integer, ForeignKey("house_info.id"))
    device_id = Column(Integer, ForeignKey("devices.id"))
    event_time = Column(DateTime)
    event_type = Column(String)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)  # ✅ 添加主键
    user_id = Column(Integer, ForeignKey("users.id"))
    feedback_text = Column(String)
    feedback_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")
