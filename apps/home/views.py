"""Views for the home app."""
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

@login_required
def index_view(request: HttpRequest) -> HttpResponse:
    """
    Render the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered home page.
    """
    return render(request, "home.html")