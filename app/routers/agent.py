# app/routers/agent.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.agent.query_parser import parse_query  # ✅ 自定义的查询解析器
import matplotlib.pyplot as plt
import io
import base64

router = APIRouter()

@router.post("/agent")
def agent_analysis(request: dict, db: Session = Depends(get_db)):
    """
    根据自然语言分析请求并返回 SQL 执行结果或图表（base64）。
    示例输入：{"query": "分析不同房屋面积下空调的使用次数"}
    """
    nl_query = request.get("query", "").strip()
    if not nl_query:
        raise HTTPException(status_code=400, detail="请提供 query 字段。")

    sql = parse_query(nl_query)

    if not sql:
        raise HTTPException(status_code=400, detail="无法解析该分析请求。")

    try:
        result = db.execute(sql).fetchall()

        if not result:
            return {"result": [], "note": "未查询到结果"}

        # 如果包含面积 + 空调关键词，就画图
        if "area" in sql and "ac_usage" in sql:
            labels = [str(row[0]) for row in result]
            values = [row[1] for row in result]

            plt.figure(figsize=(8, 6))
            plt.bar(labels, values, color="skyblue")
            plt.title("不同房屋面积的空调使用次数")
            plt.xlabel("房屋面积区间")
            plt.ylabel("使用次数")
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            plt.close()
            buf.seek(0)
            encoded = base64.b64encode(buf.read()).decode("utf-8")

            return {
                "image_base64": encoded,
                "raw": [dict(r._mapping) for r in result]
            }

        # 否则返回普通查询结果
        return {
            "result": [dict(r._mapping) for r in result]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析执行错误: {str(e)}")
