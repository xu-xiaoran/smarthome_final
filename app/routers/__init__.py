# app/routers/__init__.py

from fastapi import APIRouter
from app.routers import user, house, device, usage_record, security_event, user_feedback
from app.routers import agent, openai_agent
from app.routers import analysis  # 新增导入 analysis 模块

router = APIRouter()

# 原有资源路由
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(house.router, prefix="/houses", tags=["houses"])
router.include_router(device.router, prefix="/devices", tags=["devices"])
router.include_router(usage_record.router, prefix="/usage_records", tags=["usage_records"])
router.include_router(security_event.router, prefix="/security_events", tags=["security_events"])
router.include_router(user_feedback.router, prefix="/user_feedbacks", tags=["user_feedbacks"])

# 分析相关路由

router.include_router(openai_agent.router, prefix="/analytics", tags=["Analytics"])
router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])  # 新增统一分析接口