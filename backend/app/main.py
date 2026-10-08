
from fastapi import FastAPI

from app.db.database import Base, engine

from app.models import (
    User,
    Office,
    Service,
    QueueEntry,
    Appointment,
)


from app.api import queue, users, services, staff, appointments, feedback

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Kabale University Digital Queue System",
    description="Queue and appointment management system for student support services.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(queue.router)
app.include_router(services.router)
app.include_router(staff.router)
app.include_router(appointments.router)
app.include_router(feedback.router)


@app.get("/")
def root():
    return {
        "message": "Kabale University Digital Queue System API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}