"""Video application views module."""

import os
from os.path import abspath, dirname, join
from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from levai import settings
from levai.apps.video.backend.audio import video_to_mp3_moviepy
from levai.apps.video.backend.conversor import convert_to_mp4_moviepy
from levai.apps.video.backend.video import download_video_hd
from levai.core.constants import TEMP_VIDEO_FILE_NAME
from levai.core.utils.enums import UploadDirs
from levai.core.utils.upload import save_uploaded_file


@login_required
def download_view(request: HttpRequest) -> HttpResponse | FileResponse:
    """Download a video by URL and return it as a file response.

    Args:
        request (HttpRequest): The request object containing the video
            URL and file name in POST data.

    Returns:
        HttpResponse | FileResponse: A file response with the downloaded
            video, or the rendered download form.

    """
    if request.method == "POST":
        url: str | None = request.POST.get("url")
        file_name: str | None = request.POST.get("file_name")
        if url:

            file_path: str | None = download_video_hd(url)

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

            return FileResponse(
                open(file_path, "rb"),
                as_attachment=True,
                filename=file_name + ".mp4",
            )

        else:
            messages.error(request, "Erro ao baixar o vídeo.")

    return render(request, "video_download.html")


@login_required
def convert_video_to_audio(request: HttpRequest) -> HttpResponse:
    """Convert a video file to MP3 and offer it for download.

    Args:
        request (HttpRequest): The request object containing the video
            file in FILES data.

    Returns:
        HttpResponse: A file response with the MP3 audio, or the
            rendered conversion form.

    """
    if request.method == "POST":
        video_file = request.FILES.get("video")

        if video_file:
            try:
                video_path: str = save_uploaded_file(video_file, UploadDirs.VIDEOS)
                full_video_path: str = os.path.join(settings.MEDIA_ROOT, video_path)

                mp3_path: str = video_to_mp3_moviepy(full_video_path)

                return FileResponse(
                    open(mp3_path, "rb"),
                    as_attachment=True,
                    filename=f"{Path(video_file.name).stem}.mp3",
                )

            except Exception as e:
                messages.error(request, f"Erro na conversão: {e}")

        else:
            messages.error(request, "Nenhum vídeo selecionado!")

    return render(request, "video_to_audio.html")


@login_required
def convert_to_mp4_view(request: HttpRequest) -> HttpResponse:
    """Convert a video file to MP4 and offer it for download.

    Args:
        request (HttpRequest): The request object containing the video
            file in FILES data.

    Returns:
        HttpResponse: A file response with the MP4 video, or a redirect
            to the conversion form.

    """
    if request.method == "POST":
        video_file = request.FILES.get("video")

        if not video_file:
            messages.error(request, "Nenhum vídeo selecionado!")
            return redirect("convert_to_mp4")

        allowed_extensions: list[str] = [
            ".mov",
            ".avi",
            ".mkv",
            ".wmv",
            ".flv",
            ".webm",
            ".m4v",
        ]
        file_extension: str = Path(video_file.name).suffix.lower()

        if file_extension not in allowed_extensions:
            messages.error(
                request,
                f"""
                Formato não suportado: {file_extension}.
                Use: {', '.join(allowed_extensions)}
                """,
            )
            return redirect("convert_to_mp4")

        try:
            video_path: str = save_uploaded_file(video_file, UploadDirs.VIDEOS)
            full_video_path: str = os.path.join(settings.MEDIA_ROOT, video_path)

            mp4_path: str = convert_to_mp4_moviepy(full_video_path)

            if os.path.exists(mp4_path):
                original_name: str = Path(video_file.name).stem
                download_filename: str = f"{original_name}_converted.mp4"

                response: FileResponse = FileResponse(
                    open(mp4_path, "rb"),
                    as_attachment=True,
                    filename=download_filename,
                )

                return response
            else:
                messages.error(request, "Erro: Arquivo MP4 não foi gerado.")

        except FileNotFoundError as e:
            messages.error(request, f"Arquivo não encontrado: {e}")
        except Exception as e:
            messages.error(request, f"Erro na conversão: {str(e)}")

        return redirect("convert_to_mp4")

    return render(request, "convert_to_mp4.html")
