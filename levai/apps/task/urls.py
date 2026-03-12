"""URL configuration for the task application."""

from django.urls import path

from levai.apps.task.views import (
    task_create_view,
    task_delete_view,
    task_detail_json_view,
    task_update_view,
    task_view,
)

urlpatterns = [
    path("", task_view, name="task_view"),
    path("create/", task_create_view, name="task_create"),
    path("<uuid:task_id>/", task_detail_json_view, name="task_detail_json"),
    path("<uuid:task_id>/update/", task_update_view, name="task_update"),
    path("<uuid:task_id>/delete/", task_delete_view, name="task_delete"),
]
