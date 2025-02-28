from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from sqlmodel import Session, select

from dependencies import get_db, get_user, templates
from models.notes import CreateNote, Note, UpdateNote
from models.users import User


router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[Note])
def get_notes(
    request: Request,
    user: Annotated[User, Depends(get_user)],
    session: Annotated[Session, Depends(get_db)],
    note_id: Annotated[int, Query(alias="v")] = None,
):
    notes = session.exec(
        select(Note).where(Note.user_id == user.id).order_by(Note.created_at.desc())
    ).all()
    note = None

    if note_id:
        note = session.get(Note, note_id)
        if note.user_id != user.id:
            note = None

    context = {"notes": notes, "existingNote": note}
    return templates.TemplateResponse(request, "main/notes/notes.html", context)


@router.post("/", response_model=Note)
async def create_note(
    payload: Annotated[CreateNote, Form()],
    request: Request,
    user: Annotated[User, Depends(get_user)],
    session: Annotated[Session, Depends(get_db)],
):
    note = Note(**payload.model_dump(), user_id=user.id)

    session.add(note)
    session.commit()
    session.refresh(note)

    response = get_notes(request, user=user, session=session, note_id=note.id)
    response.headers.append("HX-Replace-Url", f"?v={note.id}")
    return response


@router.put("/", response_model=Note)
async def update_note(
    payload: Annotated[UpdateNote, Form()],
    request: Request,
    user: Annotated[User, Depends(get_user)],
    session: Annotated[Session, Depends(get_db)],
):
    note = session.get(Note, payload.id)
    if not note or note.user_id != user.id:
        return HTTPException(status_code=403)

    note.sqlmodel_update(payload.model_dump())
    session.add(note)
    session.commit()
    session.refresh(note)

    return get_notes(request, user=user, session=session, note_id=note.id)


@router.delete("/")
async def delete_note(
    request: Request,
    user: Annotated[User, Depends(get_user)],
    session: Annotated[Session, Depends(get_db)],
    note_id: Annotated[int, Query(alias="v")] = None,
):
    print(note_id)
    note = session.get(Note, note_id)
    if not note or note.user_id != user.id:
        return HTTPException(status_code=403)

    session.delete(note)
    session.commit()

    response = get_notes(request, user=user, session=session)
    response.headers.append("HX-Replace-Url", "/notes")
    return response
