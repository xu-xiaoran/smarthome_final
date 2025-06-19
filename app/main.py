# app/main.py

from fastapi import FastAPI
from app import models
from app.database import engine, Base
from app.routers import router  # ✅ 加载 __init__.py 中封装好的 router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="智能家居系统 API")

app.include_router(router)  # ✅ 只注册这个总路由

@app.get("/")
def read_root():
    return {"message": "欢迎使用智能家居系统 API"}
