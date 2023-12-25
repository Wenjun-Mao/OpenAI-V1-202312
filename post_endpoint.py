from typing import Optional
from urllib.parse import unquote

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from utils_net import (
    create_incoming_file_path,
    save_incoming_file,
)

from utils_pic import (
    create_expanded_and_mask_images,
    get_img_desc,
    get_expanded_img_url,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    await save_incoming_file(file, url, incoming_file_path)

    # Create the expanded and mask images
    expanded_image_path, mask_image_path = create_expanded_and_mask_images(
        incoming_file_path, 1024
    )
    # Get the image description
    img_desc = get_img_desc(incoming_file_path)

    # Get the expanded image url
    expanded_image_url = get_expanded_img_url(
        expanded_image_path, mask_image_path, img_desc, n=1, size="1024x1024"
    )

    return JSONResponse(
        content={
            "expanded_image_url": expanded_image_url,
            "id_value": id_value,
            "img_desc": img_desc,
        }
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9631, log_level="info")
