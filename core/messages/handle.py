"""Handle messages for success and error notifications in Django."""

from django.contrib import messages
from django.http import HttpRequest


def handle_error_message(request: HttpRequest, error: Exception) -> None:
    """Handle error messages by displaying them to the user.

    Args:
        request (HttpRequest): The HTTP request object.
        error (Exception): The exception to handle.

    Returns:
        None

    """
    messages.error(request, str(error))


def handle_success_message(request: HttpRequest, message: str) -> None:
    """Handle error messages by displaying them to the user.

    Args:
        request (HttpRequest): The HTTP request object.
        message (str): The success message to display.

    Returns:
        None

    """
    messages.success(request, message)
