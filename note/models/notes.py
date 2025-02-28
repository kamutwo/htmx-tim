from sqlmodel import SQLModel, Field
from datetime import datetime


class BaseNote(SQLModel):
    title: str
    content: str


class Note(BaseNote, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, index=True, foreign_key="user.id")

    created_at: datetime = Field(default_factory=datetime.now)


class CreateNote(BaseNote):
    pass


class UpdateNote(BaseNote):
    id: int
