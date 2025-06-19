# app/routers/analysis.py

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
import re
import matplotlib.pyplot as plt
import matplotlib
import io
import base64
from collections import defaultdict

# Matplotlib 设置
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

router = APIRouter(prefix="/analysis", tags=["Analysis"])

# 设备类型映射
DEVICE_TYPE_MAP = {
    "空调": "AC", "灯": "Light", "门锁": "Lock", "摄像头": "Camera",
    "电视": "TV", "风扇": "Fan", "加湿器": "Humidifier",
    "窗帘": "Curtain", "音响": "Speaker"
}

def map_device_type(device_type: str) -> str:
    return DEVICE_TYPE_MAP.get(device_type.strip(), device_type)

def execute_sql(db: Session, sql: str):
    try:
        result = db.execute(text(sql)).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL执行失败：{str(e)}")

# ------------------ 数据分析接口 ------------------

def device_usage_sql():
    return """
    SELECT d.device_type,
           COUNT(*) AS total_usage,
           SUM(CASE WHEN EXTRACT(HOUR FROM ur.start_time) BETWEEN 0 AND 5 THEN 1 ELSE 0 END) AS late_night,
           SUM(CASE WHEN EXTRACT(HOUR FROM ur.start_time) BETWEEN 6 AND 11 THEN 1 ELSE 0 END) AS morning,
           SUM(CASE WHEN EXTRACT(HOUR FROM ur.start_time) BETWEEN 12 AND 17 THEN 1 ELSE 0 END) AS afternoon,
           SUM(CASE WHEN EXTRACT(HOUR FROM ur.start_time) BETWEEN 18 AND 23 THEN 1 ELSE 0 END) AS evening
    FROM usage_records ur
    JOIN devices d ON ur.device_id = d.id
    GROUP BY d.device_type
    ORDER BY total_usage DESC;
    """

def co_usage_sql():
    return """
    WITH overlapping_usages AS (
        SELECT
            ur1.user_id,
            ur1.device_id AS device_id_1,
            ur2.device_id AS device_id_2,
            COUNT(*) AS overlap_count
        FROM usage_records ur1
        JOIN usage_records ur2
          ON ur1.user_id = ur2.user_id
         AND ur1.device_id < ur2.device_id
         AND ur1.start_time < ur2.end_time
         AND ur2.start_time < ur1.end_time
        GROUP BY ur1.user_id, ur1.device_id, ur2.device_id
    )
    SELECT
        ou.user_id,
        d1.device_type AS device_type_1,
        d2.device_type AS device_type_2,
        ou.overlap_count
    FROM overlapping_usages ou
    JOIN devices d1 ON ou.device_id_1 = d1.id
    JOIN devices d2 ON ou.device_id_2 = d2.id
    ORDER BY ou.user_id, ou.overlap_count DESC;
    """

def area_usage_sql():
    return """
    WITH house_area_group AS (
        SELECT id AS house_id,
               CASE 
                   WHEN area_sqm < 50 THEN '<50 sqm'
                   WHEN area_sqm BETWEEN 50 AND 99 THEN '50-99 sqm'
                   WHEN area_sqm BETWEEN 100 AND 149 THEN '100-149 sqm'
                   ELSE '150+ sqm'
               END AS area_group
        FROM houses
    ),
    house_usage AS (
        SELECT h.area_group, COUNT(ur.id) AS total_usage, COUNT(DISTINCT h.house_id) AS house_count
        FROM house_area_group h
        JOIN devices d ON h.house_id = d.house_id
        JOIN usage_records ur ON d.id = ur.device_id
        GROUP BY h.area_group
    )
    SELECT area_group, total_usage, house_count, 
           ROUND(total_usage::numeric / house_count, 2) AS avg_usage_per_house
    FROM house_usage
    ORDER BY area_group;
    """

def parse_user_query(user_query: str):
    q = user_query.lower()

    if re.search(r"(使用频率|使用时间段|device usage)", q):
        return device_usage_sql(), "设备使用频率和时间段分析"

    elif re.search(r"(使用习惯|同时使用|共现|co-usage|组合)", q):
        return co_usage_sql(), "用户设备共用习惯分析"

    elif re.search(r"(面积.*使用|area.*usage|房屋面积)", q):
        return area_usage_sql(), "房屋面积与设备使用关系分析"

    else:
        return None, None

@router.post("/query")
def analysis_query(nl_query: str = Body(..., embed=True), db: Session = Depends(get_db)):
    sql, query_type = parse_user_query(nl_query)
    if not sql:
        raise HTTPException(status_code=400, detail="暂时无法理解您的问题，请换种表达方式。")

    result = execute_sql(db, sql)

    for row in result:
        if 'device_type' in row:
            row['device_type'] = map_device_type(row['device_type'])
        if 'device_a' in row:
            row['device_a'] = map_device_type(row['device_a'])
        if 'device_b' in row:
            row['device_b'] = map_device_type(row['device_b'])

    return {
        "query_type": query_type,
        "result": result
    }

# ------------------ 可视化接口 ------------------

@router.get("/visualize/device-usage-frequency")
def visualize_device_usage_frequency(db: Session = Depends(get_db)):
    sql = """
    SELECT d.device_type, COUNT(ur.id) AS usage_count
    FROM usage_records ur
    JOIN devices d ON ur.device_id = d.id
    GROUP BY d.device_type
    ORDER BY usage_count DESC;
    """
    result = db.execute(text(sql)).fetchall()
    data = {map_device_type(k): v for k, v in dict(result).items()}

    plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), data.values())
    plt.title("Device Usage Frequency")
    plt.xlabel("Device Type")
    plt.ylabel("Usage Count")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')

    return {"image": f"data:image/png;base64,{img_str}"}

@router.get("/visualize/device-hourly")
def visualize_device_hourly_usage(db: Session = Depends(get_db)):
    sql = """
    SELECT EXTRACT(HOUR FROM ur.start_time) AS hour, d.device_type, COUNT(*) AS count
    FROM usage_records ur
    JOIN devices d ON ur.device_id = d.id
    GROUP BY hour, d.device_type
    ORDER BY hour;
    """
    result = db.execute(text(sql)).fetchall()

    grouped = defaultdict(list)
    for row in result:
        en_device_type = map_device_type(row.device_type)
        grouped[en_device_type].append((row.hour, row.count))

    plt.figure(figsize=(12, 6))
    for dev_type, values in grouped.items():
        hours, counts = zip(*values)
        plt.plot(hours, counts, label=dev_type, marker='o')

    plt.title("Hourly Device Usage Trends")
    plt.xlabel("Hour of Day")
    plt.ylabel("Usage Count")
    plt.legend(title="Device Type")
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')

    return {"image": f"data:image/png;base64,{img_str}"}
