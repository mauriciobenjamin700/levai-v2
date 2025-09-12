from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def custom_404_view(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Custom 404 error page."""
    return render(request, "404.html", status=404)


def custom_500_view(request: HttpRequest) -> HttpResponse:
    """Custom 500 error page."""
    return render(request, "500.html", status=500)


def custom_403_view(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Custom 403 error page."""
    return render(request, "403.html", status=403)


def custom_400_view(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Custom 400 error page."""
    return render(request, "400.html", status=400)
    return render(request, "400.html", status=400)
