from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
import os
import uuid

from core.utils.enums import UploadDirs

def save_uploaded_file(uploaded_file: UploadedFile, folder_name: UploadDirs) -> str:
    """Salva um arquivo enviado no servidor.
    
    Args:
        uploaded_file: Arquivo enviado pelo usuário
        folder_name: Nome da pasta onde salvar
        
    Returns:
        str: Caminho relativo do arquivo salvo
    """
    upload_dir = os.path.join(settings.MEDIA_ROOT, folder_name.value)
    os.makedirs(upload_dir, exist_ok=True)
    
    
    file_extension = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    file_path = os.path.join(upload_dir, unique_filename)
    
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    
    return os.path.join(folder_name.value, unique_filename)