"""Enum definitions for the project."""

from enum import Enum


class BaseEnum(Enum):
    """Base Enum class to ensure all enums in the project inherit from this.

    Provides utility methods for accessing enum choices, keys,
    and values, as well as string representations.

    """

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        """Return all enum members as a list of (name, value) tuples.

        Returns:
            list[tuple[str, str]]: List of (name, value) pairs.

        """
        return [(item.name, item.value) for item in cls]

    @classmethod
    def keys(cls) -> list[str]:
        """Return all enum member names.

        Returns:
            list[str]: List of enum member names.

        """
        return [item.name for item in cls]

    @classmethod
    def values(cls) -> list[str]:
        """Return all enum member values.

        Returns:
            list[str]: List of enum member values.

        """
        return [item.value for item in cls]

    def __str__(self) -> str:
        """Return the string representation of the enum value.

        Returns:
            str: The string representation of the enum value.

        """
        return str(self.value)

    def __repr__(self) -> str:
        """Return a detailed string representation of the enum instance.

        Returns:
            str: A string in the format ClassName.MEMBER(value).

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


class TaskPriority(BaseEnum):
    """Enum representing the priority level of a task.

    Attributes:
        LOW: Low priority task.
        MEDIUM: Medium priority task.
        HIGH: High priority task.

    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(BaseEnum):
    """Enum representing the status of a task.

    Attributes:
        PENDING: Task has not been started.
        IN_PROGRESS: Task is currently being worked on.
        DONE: Task has been completed.

    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
