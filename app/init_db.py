from app.database import engine
from app.models.models import Base

# 创建所有表
Base.metadata.create_all(bind=engine)
print("✅ 数据表创建完成")
