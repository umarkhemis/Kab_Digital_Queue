
from app.db.database import SessionLocal
from app.models.office import Office
from app.models.service import Service


def seed():
    db = SessionLocal()

    if db.query(Office).count() > 0:
        print("Database already seeded.")
        db.close()
        return

    registrar = Office(
        name="Academic Registrar",
        description="Academic records and related services",
    )

    finance = Office(
        name="Finance",
        description="Financial and fee-related services",
    )

    student_affairs = Office(
        name="Student Affairs",
        description="Student welfare and support services",
    )

    db.add_all([registrar, finance, student_affairs])
    db.commit()

    services = [
        Service(
            office_id=registrar.id,
            name="Academic Transcript",
            description="Request an academic transcript",
        ),
        Service(
            office_id=registrar.id,
            name="Academic Inquiry",
            description="General academic inquiry",
        ),
        Service(
            office_id=finance.id,
            name="Fee Statement",
            description="Request a student fee statement",
        ),
        Service(
            office_id=finance.id,
            name="Financial Inquiry",
            description="General financial inquiry",
        ),
        Service(
            office_id=student_affairs.id,
            name="ID Replacement",
            description="Request replacement of student identification card",
        ),
        Service(
            office_id=student_affairs.id,
            name="Student Affairs Inquiry",
            description="General student affairs support",
        ),
    ]

    db.add_all(services)
    db.commit()

    print("Database seeded successfully.")

    db.close()


if __name__ == "__main__":
    seed()