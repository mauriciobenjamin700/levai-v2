"""Video Views."""

from os.path import abspath, dirname, join

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render

from apps.video.backend.video import download_video_hd
from core.constants import TEMP_VIDEO_FILE_NAME


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
