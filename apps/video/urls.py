"""Videos URLS."""

from django.urls import path

from apps.video.views import convert_video_to_audio, convert_to_mp4_view, download_view

urlpatterns = [
    path("", download_view, name="download_view"),
    path('convert/', convert_video_to_audio, name='video_to_audio'),
    path('convert-to-mp4', convert_to_mp4_view, name='convert_to_mp4_view'),

]
