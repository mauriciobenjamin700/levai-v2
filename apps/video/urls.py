"""Videos URLS."""

from django.urls import path

from apps.video.views import download_view

urlpatterns = [
    path("", download_view, name="download_view"),
]
