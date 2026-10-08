
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.queue import QueueEntry

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.get("/queue/{service_id}")
def view_queue(
    service_id: int,
    db: Session = Depends(get_db),
):
    entries = (
        db.query(QueueEntry)
        .filter(
            QueueEntry.service_id == service_id,
            QueueEntry.status.in_(["waiting", "called", "serving"]),
        )
        .order_by(QueueEntry.queue_number)
        .all()
    )

    return [
        {
            "id": entry.id,
            "queue_number": entry.queue_number,
            "user_id": entry.user_id,
            "status": entry.status,
            "joined_at": entry.joined_at,
        }
        for entry in entries
    ]


@router.post("/queue/{service_id}/next")
def call_next(
    service_id: int,
    db: Session = Depends(get_db),
):
    entry = (
        db.query(QueueEntry)
        .filter(
            QueueEntry.service_id == service_id,
            QueueEntry.status == "waiting",
        )
        .order_by(QueueEntry.queue_number)
        .first()
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="No students are waiting in this queue",
        )

    entry.status = "called"
    entry.called_at = datetime.utcnow()

    db.commit()
    db.refresh(entry)

    return {
        "message": "Next student called",
        "queue_number": entry.queue_number,
        "queue_id": entry.id,
        "status": entry.status,
    }


@router.post("/queue/{queue_id}/start")
def start_service(
    queue_id: int,
    db: Session = Depends(get_db),
):
    entry = db.query(QueueEntry).filter(QueueEntry.id == queue_id).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Queue entry not found")

    entry.status = "serving"
    entry.service_started_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Service started",
        "queue_number": entry.queue_number,
        "status": entry.status,
    }


@router.post("/queue/{queue_id}/complete")
def complete_service(
    queue_id: int,
    db: Session = Depends(get_db),
):
    entry = db.query(QueueEntry).filter(QueueEntry.id == queue_id).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Queue entry not found")

    entry.status = "completed"
    entry.completed_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Service completed",
        "queue_number": entry.queue_number,
        "status": entry.status,
    }