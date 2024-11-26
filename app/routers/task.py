from fastapi import APIRouter, Depends, status, HTTPException
from slugify import slugify
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from typing import Annotated

from app.backend.db_depends import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateTask, UpdateTask

router = APIRouter(prefix='/tasks', tags=['tasks'])

# Все активные задачи
@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task).where(Task.is_active == True)).all()
    return tasks

# Задача по ID
@router.get('/{task_id}')
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return task

# Создать
@router.post('/create')
async def create_task(create_task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    # Проверяем, есть ли пользователь с таким user_id
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        # Если пользователь не найден, создаем его
        new_user = User(
            name=f"User{user_id}",  # Пример имени для нового пользователя, можно сделать динамическим
            slug=slugify(f"User{user_id}")
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user  # Присваиваем созданного пользователя переменной user

    # Создание задачи и связывание с пользователем
    new_task = Task(
        name=create_task.title,
        description=create_task.content,
        priority=create_task.priority,
        user_id=user.id  # Связываем задачу с найденным или только что созданным пользователем
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful',
        'task': new_task
    }

# Обновить задачу
@router.put('/update')
async def update_task(task_id: int, update_task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')

    db.execute(update(Task).where(Task.id == task_id).values(
        title=update_task.title,
        content=update_task.content,
        priority=update_task.priority
    ))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful'
    }

# Удалить задачу
@router.delete('/delete')
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')

    db.execute(update(Task).where(Task.id == task_id).values(is_active=False))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful'
    }
