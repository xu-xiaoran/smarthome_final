from sqlalchemy import Column, String, Integer, BigInteger, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class UserFeedback(Base):
    __tablename__ = 'user_feedbacks'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, index=True)
    event_id = Column(BigInteger, ForeignKey('security_events.id'), nullable=True, index=True)
    feedback_text = Column(String, nullable=False)
    feedback_time = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    feedback_type = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    user = relationship("User", back_populates="feedbacks")
    security_event = relationship(
        "SecurityEvent",
        backref="feedbacks",  # 允许反向查找 event.feedbacks
        foreign_keys=[event_id]
    )
