# app/routers/house.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/houses",
    tags=["houses"],
)

@router.post("/", response_model=schemas.house.House, status_code=status.HTTP_201_CREATED)
def create_house(house: schemas.house.HouseCreate, db: Session = Depends(get_db)):
    # 检查所属用户是否存在
    db_user = crud.user.get_user_by_id(db, house.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="所属用户不存在")
    return crud.house.create_house(db, house)

@router.get("/{house_id}", response_model=schemas.house.House)
def read_house(house_id: int, db: Session = Depends(get_db)):
    db_house = crud.house.get_house_by_id(db, house_id)
    if not db_house:
        raise HTTPException(status_code=404, detail="房屋不存在")
    return db_house

@router.get("/", response_model=List[schemas.house.House])
def list_houses_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    houses = crud.house.get_houses_by_user(db, user_id)
    return houses

@router.delete("/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_house(house_id: int, db: Session = Depends(get_db)):
    success = crud.house.delete_house(db, house_id)
    if not success:
        raise HTTPException(status_code=404, detail="房屋不存在")
    return

@router.put("/{house_id}", response_model=schemas.house.House)
def update_house(house_id: int, house_update: schemas.house.HouseCreate, db: Session = Depends(get_db)):
    db_house = crud.house.get_house_by_id(db, house_id)
    if not db_house:
        raise HTTPException(status_code=404, detail="房屋不存在")
    update_data = house_update.dict(exclude_unset=True)
    house_obj = crud.house.update_house(db, house_id, **update_data)
    return house_obj
