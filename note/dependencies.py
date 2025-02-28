from typing import Annotated
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from core.database import engine
from core.security import OAuth2CookiePasswordBearer
from models.users import User
from core.auth import decode_token


templates = Jinja2Templates("templates")
bearer = OAuth2CookiePasswordBearer(tokenUrl="/auth/token")


async def get_db():
    with Session(engine) as session:
        yield session


async def get_user(
    token: Annotated[str, Depends(bearer)],
    session: Annotated[Session, Depends(get_db)],
):
    claims = decode_token(token)
    if not claims.get("user_id"):
        return None

    user = session.get(User, claims.get("user_id"))
    return user
