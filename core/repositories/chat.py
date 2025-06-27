from apps.chat.models import Chat, ChatMessage
from core.schemas import ChatMessageRequest, ChatMessageResponse, ChatRequest, ChatResponse
from core.utils.enums import ChatRole

class ChatRepository:
    """
    Repository for managing chat sessions and messages.
    """

    @staticmethod
    def create_chat(user_id: str) -> Chat:
        """
        Create a new chat session for a user.
        
        Args:
            user_id (str): The ID of the user starting the chat.
        
        Returns:
            Chat: The created chat session.
        """
        chat = Chat(user_id=user_id)
        return chat

    @staticmethod
    def add_chat(model: Chat) -> Chat:
        """
        Create a new chat session for a user.
        
        Args:
            user_id (str): The ID of the user starting the chat.
        
        Returns:
            Chat: The created chat session.
        """
        
        model.full_clean()
        model.save()
        return model
    
    @staticmethod
    def get_chat(chat_id: str) -> Chat:
        """
        Retrieve a chat session by its ID.
        
        Args:
            chat_id (str): The ID of the chat session to retrieve.
        
        Returns:
            Chat: The chat session if found, otherwise raises an error.
        """
        return Chat.objects.get(id=chat_id)
    
    @staticmethod
    def get_all_chats(user_id: str | None = None) -> list[Chat]:
        """
        Retrieve all chat sessions, optionally filtered by user ID.

        Args:
            user_id (str, optional): The ID of the user to filter chats by.
        Returns:
            list[Chat]: List of chat sessions. If user_id is provided, returns chats for that user.
        """
        if user_id:
            return list(Chat.objects.filter(user_id=user_id).order_by('-created_at'))
        return list(Chat.objects.all().order_by('-created_at'))
    
    
    @staticmethod
    def update_chat(model: Chat) -> Chat:
        """
        Update an existing chat session.
        
        Args:
            model (Chat): The chat model instance to be updated.
        
        Returns:
            Chat: The updated chat model instance.
        """
        model.full_clean()
        model.save()
        return model
    
    @staticmethod
    def delete_chat(
        chat_id: str | None = None,
        chat: Chat | None = None,
    ) -> None:
        """
        Delete a chat session by its ID.
        
        Args:
            chat_id (str): The ID of the chat session to delete.
        
        Returns:
            None
        """
        if chat_id:
            chat = Chat.objects.get(id=chat_id)
            chat.delete()
        elif chat:
            chat.delete()
        else:
            raise ValueError("Either chat_id or chat must be provided to delete a chat session.")

    @staticmethod
    def create_chat_message(chat_id: str, role: str, content: str) -> ChatMessage:
        """
        Create a new chat message in a chat session.
        
        Args:
            chat_id (str): The ID of the chat session.
            role (str): The role of the message sender (user, assistant, system).
            content (str): The content of the message.
        
        Returns:
            ChatMessage: The created chat message.
        """

        if role not in ChatRole.values():
            raise ValueError(f"Invalid role: {role}. Must be one of {ChatRole.values()}.")

        message = ChatMessage(chat_id=chat_id, role=role, content=content)
        return message
    
    @staticmethod
    def add_chat_message(model: ChatMessage) -> ChatMessage:
        """
        Add a new chat message to the database.
        
        Args:
            model (ChatMessage): The chat message model instance to be added.
        
        Returns:
            ChatMessage: The added chat message model instance.
        """

        if model.role not in ChatRole.values():
            raise ValueError(f"Invalid role: {model.role}. Must be one of {ChatRole.values()}.")
        
        chat_id = model.chat_id

        if not Chat.objects.filter(id=chat_id).exists():
            raise ValueError(f"Chat with ID {chat_id} does not exist.")

        model.full_clean()

        model.save()
        
        return model
    
    @staticmethod
    def get_chat_messages(chat_id: str) -> list[ChatMessage]:
        """
        Retrieve all messages in a chat session.
        
        Args:
            chat_id (str): The ID of the chat session.
        
        Returns:
            list[ChatMessage]: List of chat messages in the session.
        """
        return list(ChatMessage.objects.filter(chat_id=chat_id).order_by('created_at'))
    
    @staticmethod
    def update_chat_message(model: ChatMessage) -> ChatMessage:
        """
        Update an existing chat message.
        
        Args:
            model (ChatMessage): The chat message model instance to be updated.
        
        Returns:
            ChatMessage: The updated chat message model instance.
        """
        if model.role not in ChatRole.values():
            raise ValueError(f"Invalid role: {model.role}. Must be one of {ChatRole.values()}.")
        
        model.full_clean()
        model.save()
        
        return model
    
    @staticmethod
    def delete_chat_message(
        message_id: str | None = None,
        message: ChatMessage | None = None,
    ) -> None:
        """
        Delete a chat message by its ID.
        
        Args:
            message_id (str): The ID of the chat message to delete.
        
        Returns:
            None
        """
        if message_id:
            message = ChatMessage.objects.get(id=message_id)
            message.delete()
        elif message:
            message.delete()
        else:
            raise ValueError("Either message_id or message must be provided to delete a chat message.")
        

    @staticmethod
    def map_chat_request_to_model(request: ChatRequest) -> Chat:
        """
        Map a ChatRequest schema to a Chat model instance.
        
        Args:
            request (ChatRequest): The chat request schema.
        
        Returns:
            Chat: The mapped chat model instance.
        """
        return Chat(**request.to_dict())
    
    @staticmethod
    def map_chat_message_request_to_model(request: ChatMessageRequest) -> ChatMessage:
        """
        Map a ChatMessageRequest schema to a ChatMessage model instance.
        
        Args:
            request (ChatMessageRequest): The chat message request schema.
        
        Returns:
            ChatMessage: The mapped chat message model instance.
        """
        return ChatMessage(**request.to_dict())
    
    @staticmethod
    def map_chat_message_to_response(model: ChatMessage) -> ChatMessageResponse:
        """
        Map a ChatMessage model instance to a ChatMessageResponse schema.
        
        Args:
            model (ChatMessage): The chat message model instance.
        
        Returns:
            ChatMessageResponse: The mapped chat message response schema.
        """
        return ChatMessageResponse.model_validate(model, from_attributes=True)
    
    @staticmethod
    def map_chat_to_response(model: Chat) -> ChatResponse:
        """
        Map a Chat model instance to a ChatResponse schema.
        
        Args:
            model (Chat): The chat model instance.
        
        Returns:
            ChatResponse: The mapped chat response schema.
        """
        messages = ChatRepository.get_chat_messages(chat_id=model.id)
        messages_response = [
            ChatRepository.map_chat_message_to_response(message) for message in messages
        ]

        return ChatResponse(
            id=model.id,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            messages=messages_response
        )

    
