
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.db.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    appointment_time = Column(DateTime, nullable=False)

    status = Column(
        String(30),
        default="booked",
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )