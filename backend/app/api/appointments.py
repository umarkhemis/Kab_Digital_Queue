
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import get_db
from app.models.appointment import Appointment
from app.models.service import Service
from app.models.user import User

router = APIRouter(prefix="/appointments", tags=["Appointments"])


class AppointmentCreate(BaseModel):
    user_id: int
    service_id: int
    appointment_time: datetime


@router.post("/")
def book_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == data.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    service = db.query(Service).filter(Service.id == data.service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    appointment = Appointment(
        user_id=data.user_id,
        service_id=data.service_id,
        appointment_time=data.appointment_time,
        status="booked",
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment booked successfully",
        "appointment_id": appointment.id,
        "appointment_time": appointment.appointment_time,
        "status": appointment.status,
    }


@router.get("/user/{user_id}")
def get_user_appointments(
    user_id: int,
    db: Session = Depends(get_db),
):
    appointments = (
        db.query(Appointment)
        .filter(Appointment.user_id == user_id)
        .order_by(Appointment.appointment_time)
        .all()
    )

    return appointments