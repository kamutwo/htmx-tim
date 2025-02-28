import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from dependencies import get_db, templates
from models.users import User
from core.auth import encode_token, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request, name="auth/login.html")


@router.post("/token")
async def authenticate(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_db)],
):
    user = session.exec(
        select(User).where(User.username == payload.username)
    ).one_or_none()

    if not user or not verify_password(
        payload.password, user.hashed_password, user.salt
    ):
        return HTTPException(status_code=400, detail="Incorrect username or password")

    token = encode_token(claims={"uuid": uuid.uuid4().hex, "user_id": user.id})
    response = JSONResponse(
        content={"access_token": token, "token_type": "bearer"},
        headers={"HX-Redirect": "/"},
    )
    response.set_cookie("authorization", f"bearer {token}", secure=True, httponly=True)

    return response
