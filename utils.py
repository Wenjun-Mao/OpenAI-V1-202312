# utils.py

import os
import asyncio
import aiohttp
import aiofiles

from typing import Optional
from fastapi import UploadFile
from urllib.parse import urlparse, unquote


# Constants
INCOMING_FOLDER = "./api_incoming"

# Create the incoming folder if it doesn't exist
os.makedirs(INCOMING_FOLDER, exist_ok=True)


def extract_filename_from_url(url: str) -> str:
    """
    Extracts a filename from a URL, providing a default if extraction fails.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(unquote(parsed_url.path))
    return filename if filename else "default_filename"

def create_incoming_file_path(file: Optional[UploadFile], url: Optional[str]):
    if file:
        return os.path.join(INCOMING_FOLDER, file.filename)
    elif url:
        filename = extract_filename_from_url(url)
        return os.path.join(INCOMING_FOLDER, filename)
    else:
        raise ValueError("Either file or URL must be provided")


async def download_from_url_with_retry(url: str, timeout: int = 5, max_attempts: int = 3) -> bytes:
    """
    Asynchronously downloads content from a URL with retry logic.
    """
    attempts = 0
    while attempts < max_attempts:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=timeout) as response:
                    response.raise_for_status()
                    return await response.read()
        except (asyncio.TimeoutError, aiohttp.ClientError):
            attempts += 1
            await asyncio.sleep(2)  # Async sleep
    raise asyncio.TimeoutError(f"Failed to retrieve {url} after {max_attempts} attempts")


async def save_incoming_file(
    file: Optional[UploadFile], url: Optional[str], incoming_file_path: str
):
    if file:
        async with aiofiles.open(incoming_file_path, 'wb') as out_file:
            await out_file.write(await file.read())
    elif url:
        file_content = await download_from_url_with_retry(url)
        async with aiofiles.open(incoming_file_path, 'wb') as out_file:
            await out_file.write(file_content)