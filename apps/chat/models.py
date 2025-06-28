"""Models for the chat application."""

from uuid import uuid4

from django.db import models


class Chat(models.Model):
    """Model to store chat sessions.

    Attributes:
        id (int): Unique identifier for the chat session.
        user_id (int): Identifier for the user associated with the chat.
        created_at (datetime): Timestamp when the chat session was created.
        updated_at (datetime): Timestamp when the chat session was last updated.

    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Chat model."""

        db_table = "chats"
        verbose_name = "Chats"
        verbose_name_plural = "Chats"


class ChatMessage(models.Model):
    """Model to store chat messages.

    Attributes:
        id (int): Unique identifier for the message.
        chat_id (Chat): Foreign key to the Chat model.
        role (str): Role of the message sender (user, assistant, system).
        content (str): Content of the message.
        created_at (datetime): Timestamp when the message was created.

    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    chat_id = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the Chat model."""

        db_table = "chat_messages"
        verbose_name = "Chat_messages"
        verbose_name_plural = "Chat_messages"
