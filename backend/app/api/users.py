

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, LoginRequest


router = APIRouter(prefix="/users", tags=["Users"])


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must not exceed 72 bytes.",
        )
    return bcrypt.hashpw(
        password_bytes, bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False


@router.post("/", status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    email = data.email.strip().lower()

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists.",
        )

    phone = data.phone.strip() if data.phone else None

    if phone and db.query(User).filter(User.phone == phone).first():
        raise HTTPException(
            status_code=409,
            detail="An account with this phone number already exists.",
        )

    password_hash = hash_password(data.password)

    user = User(
        full_name=data.full_name.strip(),
        email=email,
        phone=phone,
        password_hash=password_hash,
        role="student",
    )

    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not create account. Check whether the email or phone is already registered.",
        )

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
    }



@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    email = data.email.strip().lower()

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="This account has been disabled.",
        )

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
    }