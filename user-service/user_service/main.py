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
    db_user = await crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return await crud.create_user(db, user)

@app.get("/users/", response_model=List[schemas.UserOut])
async def list_users(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db, offset, limit)
    return users