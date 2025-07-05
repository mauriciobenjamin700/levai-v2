"""Models for the chat application."""

from datetime import datetime
from uuid import uuid4

from django.db import models

from apps.user.models import User


def default_chat_title():
    """Default title for a chat session."""
    return f"Chat {datetime.now().strftime('%d/%m %H:%M')}"


class Chat(models.Model):
    """Model to store chat sessions.

    Attributes:
        id (int): Unique identifier for the chat session.
        title (str): Title of the chat session.
        user (User): Foreign key to the User model, representing the user who owns the
        created_at (datetime): Timestamp when the chat session was created.
        updated_at (datetime): Timestamp when the chat session was last updated.

    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(
        max_length=255, blank=True, null=False, default=default_chat_title
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the Chat instance.

        Returns:
            str: The title of the chat session.

        """
        return f"""
        id: {self.id}
        title: {self.title}
        user: {self.user.username}
        created_at: {self.created_at.strftime('%d/%m/%Y %H:%M')}
        updated_at: {self.updated_at.strftime('%d/%m/%Y %H:%M')}
        """

    class Meta:
        """Meta options for the Chat model."""

        db_table = "chats"
        verbose_name = "Chats"
        verbose_name_plural = "Chats"


class ChatMessage(models.Model):
    """Model to store chat messages.

    Attributes:
        id (int): Unique identifier for the message.
        chat (Chat): Foreign key to the Chat model.
        role (str): Role of the message sender (user, assistant, system).
        content (str): Content of the message.
        created_at (datetime): Timestamp when the message was created.

    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the Chat model."""

        db_table = "chat_messages"
        verbose_name = "Chat_messages"
        verbose_name_plural = "Chat_messages"

    def __str__(self):
        """String representation of the ChatMessage instance.

        Returns:
            str: The content of the chat message.

        """
        return f"""
        id: {self.id}
        chat: {self.chat}
        role: {self.role}
        content: {self.content}
        created_at: {
            self.created_at.strftime('%d/%m/%Y %H:%M')
            if self.created_at
            else "N/A"
        }
"""
