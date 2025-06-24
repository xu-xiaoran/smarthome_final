# 智能家居系统数据库设计与分析实现

> 本项目是西南财经大学《数据库原理与运用》课程期末项目，旨在构建一个基于 FastAPI 的智能家居系统数据库管理平台，支持设备行为存储、用户数据管理、安防事件追踪、自然语言查询与可视化分析。

## 📌 项目简介

随着物联网与智能家居技术的发展，海量设备使用数据的高效管理与分析变得尤为关键。本项目设计并实现了一个后端系统，具备如下核心功能：

- 多实体层次数据建模（用户→房屋→设备）
- 高并发支持的异步 API 接口（基于 FastAPI）
- 行为日志分区存储与索引优化
- 安防事件追踪与用户反馈管理
- 自然语言查询解析（集成 GPT）
- 多种数据分析与图形可视化接口支持

👉 [在线项目演示 API 文档](http://<host>:8000/docs)  

---

## 🗂 项目结构

```

smarthome\_final/
│
├── main.py             # 项目入口
├── database.py         # 异步数据库引擎与会话管理
├── models/             # ORM 实体定义
├── schemas/            # 请求响应体结构（Pydantic）
├── crud/               # 增删改查逻辑封装
├── routers/            # 各实体 RESTful 路由
├── agent/              # 自然语言查询解析与 GPT 代理
└── analysis/           # 数据分析与可视化模块

```

---

## 🧱 数据库设计

数据库共设计六大实体：

| 实体            | 功能简述                         |
|-----------------|----------------------------------|
| `users`         | 用户注册与权限控制               |
| `houses`        | 房屋面积、房间数量等基础信息     |
| `devices`       | 智能设备类型、位置与型号信息     |
| `usage_records` | 设备使用记录（分区存储）         |
| `security_events` | 安防事件日志与处理状态         |
| `user_feedbacks`  | 用户反馈文本、关联对象与时间戳 |

📌 使用外键严格维护参照完整性；高频字段（如时间戳）均加索引优化查询效率。

---

## 🔧 系统架构（四层分层）

1. **模型层（models）**：SQLAlchemy ORM 实现实体映射及关联关系定义。
2. **Schema 层（schemas）**：Pydantic 实现请求体验证与响应过滤。
3. **数据操作层（crud）**：封装所有业务逻辑与事务处理。
4. **接口路由层（routers）**：以 RESTful 风格暴露 API 接口。

---

## 📊 数据分析功能模块

| 分析目标 | 方法描述 |
|----------|-----------|
| 设备使用频率分析 | `/visualize/device-usage-frequency` 接口，生成柱状图 |
| 使用时间段分析 | `/visualize/device-hourly` 接口，基于小时聚合折线图 |
| 设备共现分析 | 滑动窗口 + CTE 查询，识别常见联动设备组合 |
| 面积影响分析 | 面积区间分组统计设备使用量 |
| 用户反馈挖掘 | 评分分布分析、时间段偏好、设备热力图等 |

所有图表均由后端使用 `matplotlib` 生成，经 `base64` 编码传至前端展示。

---

## 💡 自然语言查询功能

项目集成 `query_parser` 与 `openai_agent` 模块，实现如下功能：

- 将自然语言解析为 SQL 查询模板
- 复杂查询自动调用 GPT 生成 SQL
- 查询结果可选择图表输出

示例：  
```

“查询 100 平米以上房屋中最常使用的设备类型” → SQL → 图表返回

````

---

## 📎 API 示例

访问 [http://localhost:8000/docs](http://localhost:8000/docs) 进入 Swagger UI 文档，支持在线调试：

| 方法 | 路径 | 描述 |
|------|------|------|
| GET  | `/users/users/` | 获取用户列表 |
| POST | `/users/users/` | 新建用户 |
| PUT  | `/users/users/{id}` | 更新用户信息 |
| DELETE | `/users/users/{id}` | 删除用户 |
| POST | `/analysis/query` | 关键词/NL查询接口 |
| GET  | `/visualize/device-usage-frequency` | 设备使用频率图表 |

---

## 🖥️ 启动方式

```bash
# 克隆项目
git clone https://github.com/xu-xiaoran/smarthome_final.git
cd smarthome_final

# 创建虚拟环境并安装依赖
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload
````

---

## 🙌 致谢

本项目由徐潇然、彭诗涵共同开发完成，感谢陈中普老师在课程中的悉心指导。
