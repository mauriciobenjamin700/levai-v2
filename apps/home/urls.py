"""Urls for the home app."""

from django.urls import path

from apps.home.views import index_view

urlpatterns = [path("", index_view, name="home")]
