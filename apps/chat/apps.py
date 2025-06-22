"""Django application configuration for the chat app."""

from django.apps import AppConfig


class ChatConfig(AppConfig):
    """Configuration class for the chat application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.chat"
