# app/routers/security_event.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/security_events",
    tags=["security_events"],
)

@router.post("/", response_model=schemas.security_event.SecurityEvent, status_code=status.HTTP_201_CREATED)
def create_security_event(event: schemas.security_event.SecurityEventCreate, db: Session = Depends(get_db)):
    # 检查房屋是否存在
    db_house = crud.house.get_house_by_id(db, event.house_id)
    if not db_house:
        raise HTTPException(status_code=404, detail="所属房屋不存在")
    # 如果提供了 device_id，需要检查设备是否存在
    if event.device_id:
        db_device = crud.device.get_device_by_id(db, event.device_id)
        if not db_device:
            raise HTTPException(status_code=404, detail="所属设备不存在")
    return crud.security_event.create_security_event(db, event)

@router.get("/{event_id}", response_model=schemas.security_event.SecurityEvent)
def read_security_event(event_id: int, db: Session = Depends(get_db)):
    ev = crud.security_event.get_security_event_by_id(db, event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="事件不存在")
    return ev

@router.get("/by_house/{house_id}", response_model=List[schemas.security_event.SecurityEvent])
def list_events_by_house(house_id: int, db: Session = Depends(get_db)):
    return crud.security_event.get_security_events_by_house(db, house_id)

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_security_event(event_id: int, db: Session = Depends(get_db)):
    success = crud.security_event.delete_security_event(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="事件不存在")
    return

@router.put("/{event_id}", response_model=schemas.security_event.SecurityEvent)
def update_security_event(event_id: int, is_handled: bool, feedback_id: int = None, db: Session = Depends(get_db)):
    """
    用于标记事件是否已处理，并可绑定反馈ID。
    """
    updated = crud.security_event.update_security_event_handle(db, event_id, is_handled, feedback_id)
    if not updated:
        raise HTTPException(status_code=404, detail="事件不存在")
    return updated
