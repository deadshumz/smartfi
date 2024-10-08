from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Sequence

from sqlalchemy.orm.sync import update

from . import schemas, models, security


async def create_user(db: AsyncSession, user: schemas.UserIn) -> models.User:
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_users(db: AsyncSession, offset: int, limit: int) -> Sequence[models.User]:
    result = await db.execute(select(models.User).offset(offset).limit(limit))
    return result.scalars().all()


async def get_user(db: AsyncSession, user_id: int) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()


async def update_user(db: AsyncSession, user_id: int, user: schemas.UserUpdate) -> models.User:
    if user.password:
        hashed_password = security.get_password_hash(user.password)
        user.password = hashed_password

    db_user = await get_user(db, user_id)
    if db_user is None:
        raise ValueError("User not found")

    stmt = (
        update(models.User)
        .where(models.User.id == user_id)
        .values(user.model_dump())
    )
    await db.execute(stmt)
    await db.commit()
    await db.refresh(user)
    return db_user
