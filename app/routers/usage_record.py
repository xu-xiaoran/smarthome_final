# app/routers/usage_record.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/usage_records",
    tags=["usage_records"],
)

@router.post("/", response_model=schemas.usage_record.UsageRecord, status_code=status.HTTP_201_CREATED)
def create_usage_record(record: schemas.usage_record.UsageRecordCreate, db: Session = Depends(get_db)):
    # 检查设备是否存在
    db_device = crud.device.get_device_by_id(db, record.device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="设备不存在")
    # 检查用户是否存在
    db_user = crud.user.get_user_by_id(db, record.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return crud.usage_record.create_usage_record(db, record)

@router.get("/{record_id}", response_model=schemas.usage_record.UsageRecord)
def read_usage_record(record_id: int, db: Session = Depends(get_db)):
    rec = crud.usage_record.get_usage_record_by_id(db, record_id)
    if not rec:
        raise HTTPException(status_code=404, detail="记录不存在")
    return rec

@router.get("/by_device/{device_id}", response_model=List[schemas.usage_record.UsageRecord])
def list_usage_by_device(device_id: int, db: Session = Depends(get_db)):
    return crud.usage_record.get_usage_records_by_device(db, device_id)

@router.get("/by_user/{user_id}", response_model=List[schemas.usage_record.UsageRecord])
def list_usage_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.usage_record.get_usage_records_by_user(db, user_id)

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usage_record(record_id: int, db: Session = Depends(get_db)):
    success = crud.usage_record.delete_usage_record(db, record_id)
    if not success:
        raise HTTPException(status_code=404, detail="记录不存在")
    return

@router.put("/{record_id}", response_model=schemas.usage_record.UsageRecord)
def update_usage_record(record_id: int, end_time: schemas.usage_record.UsageRecordCreate, db: Session = Depends(get_db)):
    # 这里只是示范一种更新方式：用户在进行操作时，先插入 start_time，之后再传 end_time 来更新
    if not end_time.end_time:
        raise HTTPException(status_code=400, detail="必须提供 end_time 字段")
    updated = crud.usage_record.update_usage_record(db, record_id, end_time.end_time)
    if not updated:
        raise HTTPException(status_code=404, detail="记录不存在")
    return updated
