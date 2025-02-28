from http.client import HTTPResponse
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from core.database import init_db
from routers import notes, users, auth
from dependencies import bearer, templates


load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

init_db()
app.include_router(notes.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", response_class=HTTPResponse)
async def get_home(request: Request):
    return templates.TemplateResponse(request, "home.html")


@app.middleware("http")
async def verify_authorization(request: Request, call_next):
    try:
        await bearer(request=request)
    except:
        if request.url.path in ["/", "/notes"]:
            return RedirectResponse("/auth/login")
    finally:
        if request.url.path.startswith("/auth"):
            return RedirectResponse("/")

    return await call_next(request)
