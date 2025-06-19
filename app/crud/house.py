# app/crud/house.py

from sqlalchemy.orm import Session
from app.models.house import House
from app.schemas.house import HouseCreate
from typing import List, Optional

def get_house_by_id(db: Session, house_id: int) -> Optional[House]:
    return db.query(House).filter(House.id == house_id).first()

def get_houses_by_user(db: Session, user_id: int) -> List[House]:
    return db.query(House).filter(House.user_id == user_id).all()

def create_house(db: Session, house: HouseCreate) -> House:
    db_house = House(
        user_id=house.user_id,
        address=house.address,
        area_sqm=house.area_sqm,
        room_count=house.room_count
    )
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house

def delete_house(db: Session, house_id: int) -> bool:
    house_obj = db.query(House).filter(House.id == house_id).first()
    if not house_obj:
        return False
    db.delete(house_obj)
    db.commit()
    return True

def update_house(db: Session, house_id: int, **kwargs) -> Optional[House]:
    house_obj = db.query(House).filter(House.id == house_id).first()
    if not house_obj:
        return None
    for key, value in kwargs.items():
        setattr(house_obj, key, value)
    db.commit()
    db.refresh(house_obj)
    return house_obj
