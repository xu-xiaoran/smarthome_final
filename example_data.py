import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.house import House
from app.models.device import Device
from app.models.usage_record import UsageRecord
from app.models.security_event import SecurityEvent
from app.models.user_feedback import UserFeedback

Base.metadata.create_all(bind=engine)

def random_datetime(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def generate_sample_data(db: Session):
    # 清空旧数据（注意顺序）
    db.query(UserFeedback).delete()
    db.query(SecurityEvent).delete()
    db.query(UsageRecord).delete()
    db.query(Device).delete()
    db.query(House).delete()
    db.query(User).delete()
    db.commit()

    # 创建用户（5个）
    users = []
    for i in range(10):
        user = User(
            username=f"user{i+1}",
            password_hash="hashed_pw_123",
            email=f"user{i+1}@example.com",
            phone=f"1380000000{i}",
            full_name=f"用户{i+1}",
            user_type="regular"
        )
        db.add(user)
        users.append(user)
    db.commit()

    # 创建房屋（每个用户1个房屋，共5个）
    houses = []
    for user in users:
        house = House(
            user_id=user.id,
            address=f"{user.username} 的智能家居地址",
            area_sqm=round(random.uniform(80, 150), 2),
            room_count=random.randint(2, 5)
        )
        db.add(house)
        houses.append(house)
    db.commit()

    # 创建设备（每个房屋 2 台设备，共10台）
    devices = []
    for house in houses:
        for j in range(2):
            device = Device(
                house_id=house.id,
                device_name=f"{house.address}-设备{j+1}",
                device_type=random.choice(["灯", "空调", "摄像头", "门锁"]),
                location=random.choice(["客厅", "卧室", "厨房"]),
                model=f"Model-{random.randint(100, 999)}"
            )
            db.add(device)
            devices.append(device)
    db.commit()

    # 创建使用记录（20条）
    start_time = datetime.utcnow() - timedelta(days=30)
    usage_records = []
    for _ in range(500):
        user = random.choice(users)
        device = random.choice(devices)
        start = random_datetime(start_time, datetime.utcnow())
        end = start + timedelta(minutes=random.randint(5, 90))
        record = UsageRecord(
            device_id=device.id,
            user_id=user.id,
            action=random.choice(["turn_on", "turn_off", "adjust_temp"]),
            start_time=start,
            end_time=end,
            usage_duration=end - start
        )
        db.add(record)
        usage_records.append(record)
    db.commit()

    # 创建安防事件（10条）
    events = []
    for _ in range(200):
        house = random.choice(houses)
        device = random.choice(devices)
        event = SecurityEvent(
            house_id=house.id,
            device_id=device.id,
            event_type=random.choice(["入侵", "烟雾", "断电"]),
            event_time=random_datetime(start_time, datetime.utcnow()),
            description="模拟事件",
            is_handled=random.choice([True, False])
        )
        db.add(event)
        events.append(event)
    db.commit()

    # 创建用户反馈（10条）
    feedback_texts = ["不错", "卡顿", "警报太敏感", "界面清晰", "需要夜间模式"]
    for _ in range(500):
        feedback = UserFeedback(
            user_id=random.choice(users).id,
            event_id=random.choice(events).id if random.random() > 0.3 else None,
            feedback_text=random.choice(feedback_texts),
            feedback_type=random.choice(["建议", "投诉", "好评"])
        )
        db.add(feedback)
    db.commit()

    print("✅ 成功生成 20 条完整示例数据（包括用户、房屋、设备、记录、事件、反馈）")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        generate_sample_data(db)
    finally:
        db.close()
