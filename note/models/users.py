from sqlmodel import Field, SQLModel
from datetime import datetime


class BaseUser(SQLModel):
    username: str = Field(unique=True)


class User(BaseUser, table=True):
    id: int | None = Field(default=None, primary_key=True)

    hashed_password: bytes
    salt: bytes

    created_at: datetime | None = Field(default_factory=datetime.now)


class CreateUser(BaseUser):
    password: str


class PublicUser(BaseUser):
    id: int

    created_at: datetime
