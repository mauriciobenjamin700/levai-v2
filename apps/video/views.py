"""Video Views."""

import os
from os.path import abspath, dirname, join
from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from apps.video.backend.conversor import convert_to_mp4_moviepy
from apps.video.backend.video import download_video_hd
from apps.video.backend.audio import video_to_mp3_moviepy
from core.constants import TEMP_VIDEO_FILE_NAME
from core.utils.enums import UploadDirs
from core.utils.upload import save_uploaded_file
from levai import settings


@login_required
def download_view(request: HttpRequest) -> HttpResponse | FileResponse:
    """Download a video by url.

    Args:
        request (HttpRequest): The request object containing the video URL and file name

    Return:
        HttpResponse | FileResponse: A response containing the video file for download.

    """
    if request.method == "POST":
        url = request.POST.get("url")
        file_name = request.POST.get("file_name")
        print("URL: ", url)
        if url:

            file_path = download_video_hd(url)

            file_path = abspath(
                join(
                    dirname(abspath(__file__)),
                    "backend",
                    "temp",
                    file_path if file_path else TEMP_VIDEO_FILE_NAME,
                )
            )

        else:

            file_path = None

        if file_path:

            print("file_path: ", file_path)
            return FileResponse(
                open(file_path, "rb"), as_attachment=True, filename=file_name + ".mp4"
            )

        else:
            messages.error(request, "Erro ao baixar o vídeo.")

    return render(request, "video_download.html")

@login_required
def convert_video_to_audio(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        video_file = request.FILES.get('video')
        
        if video_file:
            try:
                # Salvar vídeo temporariamente
                video_path = save_uploaded_file(video_file, UploadDirs.VIDEOS)
                full_video_path = os.path.join(settings.MEDIA_ROOT, video_path)
                
                # Converter para MP3
                mp3_path = video_to_mp3_moviepy(full_video_path)
                
                # Retornar arquivo MP3 para download
                return FileResponse(
                    open(mp3_path, 'rb'),
                    as_attachment=True,
                    filename=f"{Path(video_file.name).stem}.mp3"
                )
                
            except Exception as e:
                messages.error(request, f"Erro na conversão: {e}")
        
        else:
            messages.error(request, "Nenhum vídeo selecionado!")
    
    return render(request, "video_to_audio.html")



@login_required
def convert_to_mp4_view(request: HttpRequest) -> HttpResponse:
    """Converte vídeo para MP4 e oferece download.
    
    Args:
        request (HttpRequest): Request contendo o arquivo de vídeo
        
    Returns:
        HttpResponse: Resposta com download do MP4 ou template
    """
    if request.method == "POST":
        video_file = request.FILES.get('video')
        
        if not video_file:
            messages.error(request, "Nenhum vídeo selecionado!")
            return redirect('convert_to_mp4')
        
        # Verificar formato suportado
        allowed_extensions = ['.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v']
        file_extension = Path(video_file.name).suffix.lower()
        
        if file_extension not in allowed_extensions:
            messages.error(request, f"Formato não suportado: {file_extension}. Use: {', '.join(allowed_extensions)}")
            return redirect('convert_to_mp4')
        
        try:
            # Salvar vídeo temporariamente
            video_path = save_uploaded_file(video_file, UploadDirs.VIDEOS)
            full_video_path = os.path.join(settings.MEDIA_ROOT, video_path)
            
            # Converter para MP4
            mp4_path = convert_to_mp4_moviepy(full_video_path)
            
            if os.path.exists(mp4_path):
                # Gerar nome do arquivo para download
                original_name = Path(video_file.name).stem
                download_filename = f"{original_name}_converted.mp4"
                
                # Retornar arquivo MP4 para download
                response = FileResponse(
                    open(mp4_path, 'rb'),
                    as_attachment=True,
                    filename=download_filename
                )
                
                # Opcional: Limpar arquivos temporários após um tempo
                # cleanup_temp_files.delay(full_video_path, mp4_path)  # Se usar Celery
                
                return response
            else:
                messages.error(request, "Erro: Arquivo MP4 não foi gerado.")
                
        except FileNotFoundError as e:
            messages.error(request, f"Arquivo não encontrado: {e}")
        except Exception as e:
            messages.error(request, f"Erro na conversão: {str(e)}")
            
        return redirect('convert_to_mp4')
    
    # GET request - mostrar formulário
    return render(request, "convert_to_mp4.html")