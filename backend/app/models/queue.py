
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base


class QueueEntry(Base):
    __tablename__ = "queue_entries"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    queue_number = Column(Integer, nullable=False)

    status = Column(
        String(30),
        default="waiting",
        nullable=False,
    )

    joined_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    called_at = Column(DateTime, nullable=True)

    service_started_at = Column(DateTime, nullable=True)

    completed_at = Column(DateTime, nullable=True)