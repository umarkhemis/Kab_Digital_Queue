
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.feedback import Feedback
from app.models.user import User

router = APIRouter(prefix="/feedback", tags=["Feedback"])


class FeedbackCreate(BaseModel):
    user_id: int
    queue_id: int | None = None
    rating: int
    comment: str | None = None


@router.post("/")
def submit_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
):
    if data.rating < 1 or data.rating > 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be between 1 and 5",
        )

    user = db.query(User).filter(User.id == data.user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    feedback = Feedback(
        user_id=data.user_id,
        queue_id=data.queue_id,
        rating=data.rating,
        comment=data.comment,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return {
        "message": "Feedback submitted successfully",
        "feedback_id": feedback.id,
        "rating": feedback.rating,
    }