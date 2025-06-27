"""URL configuration for the chat application."""

from django.urls import path

from apps.chat.views import chat_view

urlpatterns = [
    path("", chat_view, name="chat_view"),
]
