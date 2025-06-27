from enum import Enum


class BaseEnum(Enum):
    """
    Base Enum class to ensure all enums in the project inherit from this.
    This can be extended with common functionality for all enums if needed.
    """

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples containing the enum name and value.
        This is useful for creating choices in Django models or forms.
        """
        return [(item.name, item.value) for item in cls]
    
    @classmethod
    def keys(cls):
        """
        Returns a list of enum names.
        This can be useful for iterating over enum names.
        """
        return [item.name for item in cls]
    
    @classmethod
    def values(cls):
        """
        Returns a list of enum values.
        This can be useful for iterating over enum values.
        """
        return [item.value for item in cls]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}({self.value})"


class ChatRole(BaseEnum):
    """
    Enum representing the role of a message in a chat session.

    Attributes:
        USER: Represents a message sent by the user.
        ASSISTANT: Represents a message sent by the assistant.
        SYSTEM: Represents a system message.
    """
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"