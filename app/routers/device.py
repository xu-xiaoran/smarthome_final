# app/routers/device.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)

@router.post("/", response_model=schemas.device.Device, status_code=status.HTTP_201_CREATED)
def create_device(device: schemas.device.DeviceCreate, db: Session = Depends(get_db)):
    # 检查所属房屋是否存在
    db_house = crud.house.get_house_by_id(db, device.house_id)
    if not db_house:
        raise HTTPException(status_code=404, detail="所属房屋不存在")
    return crud.device.create_device(db, device)

@router.get("/{device_id}", response_model=schemas.device.Device)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.device.get_device_by_id(db, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="设备不存在")
    return db_device

@router.get("/", response_model=List[schemas.device.Device])
def list_devices_by_house(house_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = crud.device.get_devices_by_house(db, house_id)
    return devices

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    success = crud.device.delete_device(db, device_id)
    if not success:
        raise HTTPException(status_code=404, detail="设备不存在")
    return

@router.put("/{device_id}", response_model=schemas.device.Device)
def update_device(device_id: int, device_update: schemas.device.DeviceCreate, db: Session = Depends(get_db)):
    db_device = crud.device.get_device_by_id(db, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="设备不存在")
    update_data = device_update.dict(exclude_unset=True)
    device_obj = crud.device.update_device(db, device_id, **update_data)
    return device_obj
