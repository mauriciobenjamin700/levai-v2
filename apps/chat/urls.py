"""URL configuration for the chat application."""

from django.urls import path

from apps.chat.views import chat_view, test_chat_detail

urlpatterns = [
    path("", chat_view, name="chat_view"),
    path("<uuid:chat_id>/", chat_view, name="chat_detail"),
    path("test/<uuid:chat_id>/", test_chat_detail, name="test_chat"),  # 🧪 Teste
    path("new/", chat_view, name="new_chat_view"),
]
