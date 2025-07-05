"""URL configuration for the chat application."""

from django.urls import path

from apps.chat.views import chat_view

urlpatterns = [
    path("", chat_view, name="chat_view"),
    path("new/", chat_view, name="new_chat_view"),
    path("<str:chat_id>/", chat_view, name="chat_detail"),
]
