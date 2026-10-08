
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    user = User(
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        password_hash=data.password,
        role="student",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
    }