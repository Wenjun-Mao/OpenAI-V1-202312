import asyncio
import os

from typing import Optional
from urllib.parse import unquote

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse


app = FastAPI()

@app.post("/")
async def receive_user_request(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    id: str = Form(...),
):

    url = unquote(url) if url else None
    id_value = id

    