from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.__init__ import UserBase, UserCreate, UserUpdate
from hasher import Hasher
from dependency import get_current_user_from_token

from db.dals import UserDAL
from db.session import get_db

user_router = APIRouter()


@user_router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_dal = UserDAL(db)
    user = user.model_dump()
    user['password_hash'] = Hasher.get_password_hash(user['password_hash'])
    user['role_id'] = 1
    user['subject_type_id'] = 1
    return await user_dal.create(**user)


@user_router.get("/{user_id}")
async def read_user(user_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    user_dal = UserDAL(db)
    db_user = await user_dal.get(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.get("/")
async def read_users(current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    user_dal = UserDAL(db)
    users = await user_dal.get_all()
    return users


@user_router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    user_dal = UserDAL(db)
    db_user = await user_dal.update(user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    user_dal = UserDAL(db)
    db_user = await user_dal.delete(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")