from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy import insert
from app.models.user import User
from app.schemas import CreateUser
from slugify import slugify
from sqlalchemy import update
from sqlalchemy import select

router = APIRouter(prefix='/user', tags=['user'])

# Создаём юзера по ID
@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(name=create_user.name,
                                   parent_id=create_user.parent_id,
                                   slug=slugify(create_user.name)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }



@router.get('/all_users')
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User).where(User.is_active == True)).all()
    return users

# Обновляем
@router.put('/update_user')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: CreateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no user found'
        )

    db.execute(update(User).where(User.id == user_id).values(
            name=update_user.name,
            slug=slugify(update_user.name),
            parent_id=update_user.parent_id))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful'
    }

# Удаляем


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no user found'
        )
    db.execute(update(User).where(User.id == user_id).values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful'
    }
