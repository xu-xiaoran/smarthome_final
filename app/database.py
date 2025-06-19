from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

# 读取 .env 文件中的变量
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 创建数据库连接引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # 开启后可以在终端看到每次 ORM 执行的 SQL 语句，方便调试
)

# 创建本地会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础类，后面模型继承它
Base = declarative_base()

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("✅ 数据库连接成功！")
    except Exception as e:
        print("❌ 数据库连接失败：", e)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()