"""Custom error views for the application."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def custom_404_view(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Render the custom 404 error page.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception that triggered the 404.

    Returns:
        HttpResponse: Rendered 404 error page.

    """
    return render(request, "404.html", status=404)


def custom_500_view(request: HttpRequest) -> HttpResponse:
    """Render the custom 500 error page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered 500 error page.

    """
    return render(request, "500.html", status=500)


def custom_403_view(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Render the custom 403 error page.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception that triggered the 403.

    Returns:
        HttpResponse: Rendered 403 error page.

    """
    return render(request, "403.html", status=403)


def custom_400_view(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Render the custom 400 error page.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception that triggered the 400.

    Returns:
        HttpResponse: Rendered 400 error page.

    """
    return render(request, "400.html", status=400)
