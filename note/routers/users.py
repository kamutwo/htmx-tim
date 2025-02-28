from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session

from dependencies import get_db
from models.users import CreateUser, PublicUser, User
from core.auth import hash_password


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=PublicUser)
async def create_user(payload: CreateUser, session: Annotated[Session, Depends(get_db)]):
    hashed_password, salt = hash_password(payload.password)
    user = User(**payload.model_dump(), hashed_password=hashed_password, salt=salt)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user