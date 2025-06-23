"""Views for user authentication."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from core.messages import handle_error_message
from core.schemas import UserLogin, UserRequest
from core.services import UserService


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

                return redirect("home")

            else:
                raise ValueError("E-mail ou senha inválidos.")

        except Exception as e:
            handle_error_message(request, e)
            return redirect("login")

    return render(request, "login.html")


def logout_view(request: HttpRequest) -> HttpResponse:
    """Log out the user and redirect to the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirects to the home page after logout.

    """
    try:
        if UserService.logout(request):
            request.session.flush()
            request.user = None
            request.session.clear_expired()
            request.session.modified = True
            request.session.save()
            request.session.clear()
            request.user = None
            redirect("login")
        else:
            raise ValueError("Erro ao fazer logout. Tente novamente.")
    except Exception as e:
        handle_error_message(request, e)

    return redirect("home")