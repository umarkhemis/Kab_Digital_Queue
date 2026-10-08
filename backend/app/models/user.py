
from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(30), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(30), default="student", nullable=False)
    is_active = Column(Boolean, default=True)