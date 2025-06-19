# app/crud/device.py

from sqlalchemy.orm import Session
from app.models.device import Device
from app.schemas.device import DeviceCreate
from typing import List, Optional

def get_device_by_id(db: Session, device_id: int) -> Optional[Device]:
    return db.query(Device).filter(Device.id == device_id).first()

def get_devices_by_house(db: Session, house_id: int) -> List[Device]:
    return db.query(Device).filter(Device.house_id == house_id).all()

def create_device(db: Session, device: DeviceCreate) -> Device:
    db_device = Device(
        house_id=device.house_id,
        device_name=device.device_name,
        device_type=device.device_type,
        location=device.location,
        model=device.model
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def delete_device(db: Session, device_id: int) -> bool:
    device_obj = db.query(Device).filter(Device.id == device_id).first()
    if not device_obj:
        return False
    db.delete(device_obj)
    db.commit()
    return True

def update_device(db: Session, device_id: int, **kwargs) -> Optional[Device]:
    device_obj = db.query(Device).filter(Device.id == device_id).first()
    if not device_obj:
        return None
    for key, value in kwargs.items():
        setattr(device_obj, key, value)
    db.commit()
    db.refresh(device_obj)
    return device_obj
