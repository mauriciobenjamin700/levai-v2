"""Django application configuration for the document converter app."""

from django.apps import AppConfig


class ConverterConfig(AppConfig):
    """Configuration for the document app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.document"
