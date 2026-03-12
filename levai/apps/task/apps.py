"""Django application configuration for the task app."""

from django.apps import AppConfig


class TaskConfig(AppConfig):
    """Configuration class for the task application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "levai.apps.task"
