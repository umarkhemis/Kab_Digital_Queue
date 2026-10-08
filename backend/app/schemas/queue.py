
from pydantic import BaseModel


class QueueJoinRequest(BaseModel):
    user_id: int
    service_id: int


class QueueResponse(BaseModel):
    id: int
    queue_number: int
    status: str
    position: int

    class Config:
        from_attributes = True