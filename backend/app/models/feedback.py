
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    queue_id = Column(Integer, ForeignKey("queue_entries.id"), nullable=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)