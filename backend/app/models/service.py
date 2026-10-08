
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id"), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)