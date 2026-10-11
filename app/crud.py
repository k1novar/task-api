from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate

async def create_task(db: AsyncSession, data: TaskCreate) -> Task:
    task = Task(**data.model_dump())
    db.add(task)
    await db.flush()
    await db.refresh(task)
    return task

async def get_task(db: AsyncSession, task_id: int) -> Task | None:
    return await db.get(Task, task_id)

async def get_tasks(db: AsyncSession) -> list[Task]:
    result = await db.execute(select(Task).order_by(Task.id))
    return list(result.scalars().all())

async def update_task(db: AsyncSession, task_id: int, data: TaskUpdate) -> Task | None:
    task = await get_task(db, task_id)
    if task is None:
        return None
    
    for field, value in data.model_dump().items():
        setattr(task, field, value)

    await db.flush()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task_id: int) -> bool:
    task = await get_task(db, task_id)
    if task is None:
        return False
    await db.delete(task)
    await db.flush()
    return True