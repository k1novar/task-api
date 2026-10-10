import enum
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, String, DateTime, func

from app.database import Base

class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROCESS = "in_process"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(1000))
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"),
        default=TaskStatus.TODO,
        server_default=TaskStatus.TODO.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<Task id: {self.id}, title: {self.title!r}>"