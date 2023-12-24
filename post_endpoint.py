from typing import Optional
from urllib.parse import unquote

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

from utils_net import (
    create_incoming_file_path,
    save_incoming_file,
)

app = FastAPI()


@app.post("/")
async def receive_user_request(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    id: str = Form(...),
):
    url = unquote(url) if url else None
    id_value = id

    # Create the incoming file path
    incoming_file_path = create_incoming_file_path(file, url)

    save_incoming_file(file, url, incoming_file_path)
