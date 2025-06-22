"""Views for user authentication."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from core.messages import handle_error_message
from core.schemas import UserLogin, UserRequest
from core.services import UserService


def login_view(request: HttpRequest) -> HttpResponse:
    """Render the login page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered login page.

    """
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            result = UserService.login(
                request, UserLogin(email=email, password=password)
            )

            if result:

                return redirect("/")

            else:
                raise ValueError("E-mail ou senha inválidos.")

        except Exception as e:
            handle_error_message(request, e)
            return redirect("login")

    return render(request, "login.html")


def register_view(request: HttpRequest) -> HttpResponse:
    """Render the registration page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page.

    """
    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:

            UserService.add_user(UserRequest(name=name, email=email, password=password))

            UserService.login(request, UserLogin(email=email, password=password))

            return redirect("/")

        except Exception as e:
            handle_error_message(request, e)
            return redirect("register")

    return render(request, "register.html")
