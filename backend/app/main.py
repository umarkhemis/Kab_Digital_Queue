
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.models import User, Office, Service, QueueEntry, Appointment, Feedback
from app.api import queue, users, services, staff, appointments, feedback, statistics
from app.db.seed import seed

Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(
    title="Kabale University Digital Queue System",
    description="Queue and appointment management system for student support services.",
    version="1.0.0",
)

origins = ["http://localhost:3000"]
origins += [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
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
app.include_router(statistics.router)


@app.get("/")
def root():
    return {
        "message": "Kabale University Digital Queue System API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
