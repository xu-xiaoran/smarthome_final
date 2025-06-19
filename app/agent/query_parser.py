# app/agent/query_parser.py

def parse_query(nl_query: str) -> str:
    """
    根据自然语言查询生成预定义 SQL 查询语句。
    如果未匹配到规则，返回空字符串（可回退至 GPT）。
    """
    nl_query = nl_query.lower().strip()

    # 分析：不同设备的使用频率
    if "使用频率" in nl_query or "常用设备" in nl_query:
        return """
        SELECT d.device_type, COUNT(ur.id) AS usage_count
        FROM usage_records ur
        JOIN devices d ON ur.device_id = d.id
        GROUP BY d.device_type
        ORDER BY usage_count DESC;
        """

    # 分析：设备的使用时间段
    elif "使用时间" in nl_query or "时间段" in nl_query:
        return """
        SELECT EXTRACT(HOUR FROM ur.start_time) AS hour,
               d.device_type,
               COUNT(*) AS count
        FROM usage_records ur
        JOIN devices d ON ur.device_id = d.id
        GROUP BY hour, d.device_type
        ORDER BY hour;
        """

    # 分析：哪些设备经常一起使用
    elif "一起使用" in nl_query or "同时使用" in nl_query:
        return """
        SELECT ur1.user_id,
               d1.device_type AS device1, 
               d2.device_type AS device2,
               COUNT(*) AS co_usage_count
        FROM usage_records ur1
        JOIN usage_records ur2 
          ON ur1.user_id = ur2.user_id
         AND ur1.id < ur2.id
         AND ABS(EXTRACT(EPOCH FROM ur1.start_time - ur2.start_time)) < 300
        JOIN devices d1 ON ur1.device_id = d1.id
        JOIN devices d2 ON ur2.device_id = d2.id
        WHERE d1.id != d2.id
        GROUP BY ur1.user_id, device1, device2
        ORDER BY ur1.user_id, co_usage_count DESC;
        """


    # 分析：房屋面积对设备使用的影响
    elif "面积" in nl_query and ("空调" in nl_query or "设备" in nl_query):
        return """
        SELECT h.area_sqm, d.device_type, COUNT(*) AS usage_count
        FROM usage_records ur
        JOIN devices d ON ur.device_id = d.id
        JOIN houses h ON d.house_id = h.id
        GROUP BY h.area_sqm, d.device_type
        ORDER BY h.area_sqm;
        """

    # 子问题：用户评分反馈分布
    elif "评分" in nl_query or "反馈" in nl_query:
        return """
        SELECT uf.rating, COUNT(*) AS count
        FROM user_feedbacks uf
        GROUP BY uf.rating
        ORDER BY uf.rating;
        """

    # 默认不匹配时返回空字符串（后续可回退到 GPT）
    return ""