from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .database import AsyncSessionLocal
from . import schemas, crud

app = FastAPI()


# Dependency
def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserIn, db: AsyncSession = Depends(get_db)):
    if user.password != user.password_confirmation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords don't match")

    db_user = await crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return await crud.create_user(db, user)


@app.get("/users/", response_model=List[schemas.UserOut])
async def list_users(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db, offset, limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.UserOut)
async def update_user(user_id: int, user: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
    if user.password != user.password_confirmation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords don't match")

    try:
        result = await crud.update_user(db, user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return result
