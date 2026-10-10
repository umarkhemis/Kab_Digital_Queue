
from app.db.database import SessionLocal
from app.models.office import Office
from app.models.service import Service
from app.models.user import User

DATA = {
    "Academic Registrar": (
        "Academic records and related services",
        [("Academic Transcript", "Request an academic transcript"),
         ("Academic Inquiry", "General academic inquiry")],
    ),
    "Finance": (
        "Financial and fee-related services",
        [("Fee Statement", "Request a student fee statement"),
         ("Financial Inquiry", "General financial inquiry")],
    ),
    "Student Affairs": (
        "Student welfare and support services",
        [("ID Replacement", "Request replacement of student identification card"),
         ("Student Affairs Inquiry", "General student affairs support")],
    ),
}


def seed():
    db = SessionLocal()
    try:
        if db.query(Office).count() == 0:
            for name, (desc, services) in DATA.items():
                office = Office(name=name, description=desc)
                db.add(office)
                db.commit()
                db.refresh(office)
                for s_name, s_desc in services:
                    db.add(Service(office_id=office.id, name=s_name, description=s_desc))
                db.commit()

        if db.query(User).count() == 0:
            db.add(User(
                full_name="Ahmed Umar",
                email="ahmed@kab.ac.ug",
                phone="0700000001",
                password_hash="demo",
                role="student",
            ))
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
