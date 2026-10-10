from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import TaskStatus

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus = TaskStatus.TODO

class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime