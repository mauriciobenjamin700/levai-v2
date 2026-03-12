"""Utils module for handling file uploads in Django."""

import os
import uuid

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from levai.core.utils.enums import UploadDirs


def save_uploaded_file(uploaded_file: UploadedFile, folder_name: UploadDirs) -> str:
    """Save an uploaded file to the server with a unique filename.

    Args:
        uploaded_file (UploadedFile): The file uploaded by the user.
        folder_name (UploadDirs): The target directory enum for the upload.

    Returns:
        str: Relative path of the saved file within the media root.

    """
    upload_dir: str = os.path.join(settings.MEDIA_ROOT, folder_name.value)
    os.makedirs(upload_dir, exist_ok=True)

    file_extension: str = os.path.splitext(uploaded_file.name)[1]
    unique_filename: str = f"{uuid.uuid4()}{file_extension}"

    file_path: str = os.path.join(upload_dir, unique_filename)

    with open(file_path, "wb+") as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return os.path.join(folder_name.value, unique_filename)
