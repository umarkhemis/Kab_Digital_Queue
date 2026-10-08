
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.office import Office
from app.models.service import Service

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/offices")
def get_offices(db: Session = Depends(get_db)):
    return db.query(Office).filter(Office.is_active == True).all()


@router.get("/office/{office_id}")
def get_office_services(
    office_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(Service)
        .filter(
            Service.office_id == office_id,
            Service.is_active == True,
        )
        .all()
    )