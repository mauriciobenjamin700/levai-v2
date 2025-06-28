"""Video Views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from apps.video.backend.video import download_video


@login_required
def download_view(request: HttpRequest) -> HttpResponse:
    """Video download view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template for video download.

    """
    if request.method == "POST":
        url = request.POST.get("url")
        output = request.POST.get("output")
        file_name = request.POST.get("file_name")
        try:
            download_video(url, output, file_name)
            messages.success(request, "Download concluído com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao baixar vídeo: {e}")
        return redirect("download_view")

    return render(request, "video_download.html")
