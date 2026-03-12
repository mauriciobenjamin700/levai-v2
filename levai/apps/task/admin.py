"""Registration of task models in the Django admin interface."""

from django.contrib import admin

from levai.apps.task.models import Task

admin.site.register([Task])
