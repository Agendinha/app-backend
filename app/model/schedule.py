from pydantic import BaseModel
from datetime import datetime

class ScheduleBase(BaseModel):
    id: int
    customer_id: int
    service: str
    start_time: datetime

    class Config:
        orm_mode = True

class ScheduleCreate(BaseModel):
    customer_id: int
    service: str
    start_time: datetime

class ScheduleUpdate(BaseModel):
    customer_id: int = None
    service: str = None
    start_time: datetime = None
