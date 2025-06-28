"""Enums of project."""

from enum import Enum


class BaseEnum(Enum):
    """Base Enum class to ensure all enums in the project inherit from this."""

    @classmethod
    def choices(cls):
        """Possibles choices of enum.

        Return:
            list[str]: Values of Enum

        """
        return [(item.name, item.value) for item in cls]

    @classmethod
    def keys(cls):
        """Possibles keys of enum.

        Return:
            list[str]: Names of Enum

        """
        return [item.name for item in cls]

    @classmethod
    def values(cls):
        """Values of enum.

        Return:
            list[str]: Values of Enum

        """
        return [item.value for item in cls]

    def __str__(self):
        """Representation of the enum instance like a string.

        Args:
            None:

        Return:
            str: The string representation of the enum value.

        """
        return str(self.value)

    def __repr__(self):
        """Representation of the enum instance.

        Args:
            None:

        Return:
            str: A string representation of the enum instance.

        """
        return f"{self.__class__.__name__}.{self.name}({self.value})"


class ChatRole(BaseEnum):
    """Enum representing the role of a message in a chat session.

    Attributes:
        USER: Represents a message sent by the user.
        ASSISTANT: Represents a message sent by the assistant.
        SYSTEM: Represents a system message.

    """

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class UploadDirs(BaseEnum):
    """Enum representing the directories for file uploads.

    Attributes:
        DOCUMENTS: Directory for document uploads.
        VIDEOS: Directory for video uploads.
        IMAGES: Directory for image uploads.
        AUDIO: Directory for audio uploads.

    """

    DOCUMENTS = "documents"
    VIDEOS = "videos"
    IMAGES = "images"
    AUDIO = "audio"