"""URL configuration for user-related views."""

from django.urls import path

from apps.user.views import login_view, logout_view, register_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
]
