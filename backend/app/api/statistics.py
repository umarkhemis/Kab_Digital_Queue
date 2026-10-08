from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.queue import QueueEntry
from app.models.appointment import Appointment
from app.models.feedback import Feedback

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("/")
def get_statistics(db: Session = Depends(get_db)):

    total_queue_entries = db.query(QueueEntry).count()

    completed_services = db.query(QueueEntry).filter(
        QueueEntry.status == "completed"
    ).count()

    waiting_students = db.query(QueueEntry).filter(
        QueueEntry.status == "waiting"
    ).count()

    active_services = db.query(QueueEntry).filter(
        QueueEntry.status.in_(["called", "serving"])
    ).count()

    total_appointments = db.query(Appointment).count()

    completed_with_times = db.query(QueueEntry).filter(
        QueueEntry.joined_at.isnot(None),
        QueueEntry.service_started_at.isnot(None)
    ).all()

    waiting_times = []

    for entry in completed_with_times:
        waiting_time = (
            entry.service_started_at - entry.joined_at
        ).total_seconds() / 60

        if waiting_time >= 0:
            waiting_times.append(waiting_time)

    average_waiting_time = (
        round(sum(waiting_times) / len(waiting_times), 2)
        if waiting_times
        else 0
    )

    feedback_count = db.query(Feedback).count()

    average_rating = db.query(
        func.avg(Feedback.rating)
    ).scalar()

    average_rating = (
        round(float(average_rating), 2)
        if average_rating is not None
        else 0
    )

    return {
        "total_queue_entries": total_queue_entries,
        "completed_services": completed_services,
        "waiting_students": waiting_students,
        "active_services": active_services,
        "total_appointments": total_appointments,
        "average_waiting_time_minutes": average_waiting_time,
        "feedback_count": feedback_count,
        "average_satisfaction_rating": average_rating,
    }
