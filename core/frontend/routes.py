import os
from pathlib import Path
from http import HTTPStatus
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



front = APIRouter()

template_dir = Path(f"{os.getcwd()}/frontend/templates/")
templates = Jinja2Templates(directory=template_dir)


@front.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="get_audio.html",
        status_code=HTTPStatus.OK,    
    )
