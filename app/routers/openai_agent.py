# app/routers/openai_agent.py

import re
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from openai import OpenAI
import os
from dotenv import load_dotenv
from app.agent.query_parser import parse_query

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter(prefix="/openai", tags=["OpenAI Agent"])

def clean_sql(sql_text: str) -> str:
    cleaned = re.sub(r"```sql|```", "", sql_text, flags=re.IGNORECASE).strip()
    return cleaned

def get_schema_context():
    return """
    数据表结构：
    - users(id, username, email, phone, full_name, created_at, user_type)
    - houses(id, area_sqm, room_count, address, user_id, created_at)
    - devices(id, device_name, device_type, location, house_id, added_at)
    - usage_records(id, device_id, user_id, action, start_time, end_time, usage_duration, created_at)
    - security_events(id, house_id, device_id, event_type, event_time, is_handled, description, created_at)
    - user_feedbacks(id, user_id, event_id, feedback_text, feedback_time, feedback_type, created_at)
    """

def generate_sql_from_nl_query(nl_query: str, schema_context: str) -> str:
    system_prompt = (
        "你是一个将自然语言转换为 SQL 的助手。\n"
        "这是当前数据库的结构说明：\n"
        f"{schema_context}\n"
        "请只输出 SQL 语句，不要添加任何解释。"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": nl_query}
        ],
        temperature=0.0,
        max_tokens=300,
    )
    sql_raw = response.choices[0].message.content.strip()
    return clean_sql(sql_raw)

@router.post("/analyze")
def openai_agent_analysis(nl_query: str = Body(..., embed=True), db: Session = Depends(get_db)):
    try:
        # 先尝试规则解析
        sql_query = parse_query(nl_query)

        # 如果没有匹配规则，再用 GPT 生成 SQL
        if not sql_query:
            schema_context = get_schema_context()
            sql_query = generate_sql_from_nl_query(nl_query, schema_context)

        result = db.execute(text(sql_query)).fetchall()
        return {
            "sql": sql_query,
            "result": [dict(row._mapping) for row in result]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"错误：{str(e)}")