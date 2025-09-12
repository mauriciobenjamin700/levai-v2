"""URL configuration for the chat application."""

from django.urls import path

from levai.apps.chat.views import chat_view

urlpatterns = [
    path("", chat_view, name="chat_view"),  # /chat/
    path(
        "<uuid:chat_id>/", chat_view, name="chat_detail"
    ),  # /chat/{uuid}/  🔄 Antes de "new/"
    path("new/", chat_view, name="new_chat_view"),  # /chat/new/     🔄 Por último
]
