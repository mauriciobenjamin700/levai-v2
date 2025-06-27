from datetime import datetime
from core.schemas.base import BaseSchema
from core.utils.enums import ChatRole


class ChatRequest(BaseSchema):
    """Schema for chat request data.

    Attributes:
        user_id (str): The ID of the user initiating the chat.
    """

    user_id: str


class ChatMessageRequest(BaseSchema):
    """Schema for chat message request data.

    Attributes:
        chat_id (str): The ID of the chat session to which the message belongs.
        content (str): The content of the chat message.
        role (ChatRole): The role of the message sender (user, assistant, system).
    """

    chat_id: str
    role: ChatRole
    content: str


class ChatMessageResponse(BaseSchema):
    """Schema for chat message response data.

    Attributes:
        id (str): Unique identifier for the chat message.
        chat_id (str): The ID of the chat session to which the message belongs.
        role (ChatRole): The role of the message sender (user, assistant, system).
        content (str): The content of the chat message.
        created_at (str): Timestamp when the chat message was created.
    """

    id: str
    chat_id: str
    role: ChatRole
    content: str
    created_at: datetime
    

class ChatResponse(BaseSchema):
    """Schema for chat response data.

    Attributes:
        id (str): Unique identifier for the chat session.
        user_id (str): The ID of the user associated with the chat.
        created_at (datetime): Timestamp when the chat session was created.
        updated_at (datetime): Timestamp when the chat session was last updated.
        messages (list[ChatMessageResponse]): List of messages in the chat session.
    """

    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    messages: list[ChatMessageResponse]