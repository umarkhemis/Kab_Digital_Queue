
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.queue import QueueEntry
from app.models.service import Service
from app.models.user import User
from app.schemas.queue import QueueJoinRequest

router = APIRouter(prefix="/queue", tags=["Queue"])


@router.post("/join")
def join_queue(
    data: QueueJoinRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == data.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    service = db.query(Service).filter(Service.id == data.service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    waiting = (
        db.query(QueueEntry)
        .filter(
            QueueEntry.service_id == data.service_id,
            QueueEntry.status == "waiting",
        )
        .count()
    )

    queue_number = (
        db.query(QueueEntry)
        .filter(QueueEntry.service_id == data.service_id)
        .count()
        + 1
    )

    entry = QueueEntry(
        user_id=data.user_id,
        service_id=data.service_id,
        queue_number=queue_number,
        status="waiting",
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {
        "message": "Successfully joined queue",
        "queue_id": entry.id,
        "queue_number": queue_number,
        "position": waiting + 1,
        "status": entry.status,
    }


@router.get("/{queue_id}")
def get_queue_status(
    queue_id: int,
    db: Session = Depends(get_db),
):
    entry = db.query(QueueEntry).filter(QueueEntry.id == queue_id).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Queue entry not found")

    position = db.query(QueueEntry).filter(
        QueueEntry.service_id == entry.service_id,
        QueueEntry.status == "waiting",
        QueueEntry.queue_number <= entry.queue_number,
    ).count()

    return {
        "queue_id": entry.id,
        "queue_number": entry.queue_number,
        "status": entry.status,
        "position": position,
    }
