"""Registration of chat models in the Django admin interface."""

from django.contrib import admin

from levai.apps.chat.models import Chat, ChatMessage

admin.site.register([Chat, ChatMessage])
