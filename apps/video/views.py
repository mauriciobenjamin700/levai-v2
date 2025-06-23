from django.shortcuts import render, redirect
from django.contrib import messages
from apps.video.backend.video import download_video

def download_view(request):
    if request.method == "POST":
        url = request.POST.get("url")
        output = request.POST.get("output")
        file_name = request.POST.get("file_name")
        try:
            download_video(url, output, file_name)
            messages.success(request, "Download concluído com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao baixar vídeo: {e}")
        return redirect("video/download")
    return render(request, "video/download.html")