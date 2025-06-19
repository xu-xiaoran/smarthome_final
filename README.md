<<<<<<< HEAD
# smarthome2.0
2025-春 数据库原理期末项目
=======
# Smart Home API

这是一个基于 FastAPI 构建的智能家居系统后端项目，支持用户管理、设备管理、使用记录、安全事件及用户反馈等功能。

## 📦 技术栈

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

## 🔧 功能模块

- 用户注册与登录
- 房屋与设备绑定
- 设备使用记录追踪
- 安全事件记录与处理
- 用户反馈收集与分析
- 数据可视化分析接口

## 📂 项目结构
```plaintext
smart_home/
├── app/
│   ├── main.py               # FastAPI 程序入口
│   ├── database.py           # 数据库连接与基础配置
│   ├── models/               # 存放 SQLAlchemy ORM 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── house.py
│   │   ├── device.py
│   │   ├── usage_record.py
│   │   ├── security_event.py
│   │   └── user_feedback.py
│   ├── schemas/              # 存放 Pydantic 模型（用于请求/响应校验）
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── house.py
│   │   ├── device.py
│   │   ├── usage_record.py
│   │   ├── security_event.py
│   │   └── user_feedback.py
│   ├── crud/                 # 存放对数据库的增删改查操作封装
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── house.py
│   │   ├── device.py
│   │   ├── usage_record.py
│   │   ├── security_event.py
│   │   └── user_feedback.py
│   └── routers/              # 存放 FastAPI 路由（接口）模块
│       ├── __init__.py
│       ├── user.py
│       ├── house.py
│       ├── device.py
│       ├── usage_record.py
│       ├── security_event.py
│       └── user_feedback.py
└── venv/
```


## 启动项目

```bash
# 安装依赖
pip install -r requirements.txt

# 运行 FastAPI 应用
uvicorn app.main:app --reload
>>>>>>> a17a184 (重新上传项目代码，清空旧记录)
