"""helloapp: GET / is a page in the environment's color, GET /json the same as JSON,
GET /healthz the liveness check."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.shared.settings import settings as s

app = FastAPI(title="helloapp", version=s.VERSION)

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


def info() -> dict:
    return {
        "app": "helloapp",
        "version": s.VERSION,
        "environment": s.ENVIRONMENT,
        "color": s.COLOR,
    }


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html.j2", info())


@app.get("/json")
def json():
    return info()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
