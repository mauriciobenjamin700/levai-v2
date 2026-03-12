"""AI service module for interacting with Ollama language models."""

from ollama import ChatResponse, chat


class AIService:
    """AI service for handling text and image models using Ollama.

    Attributes:
        __text_model (str): The text generation model identifier.
        __image_model (str): The image understanding model identifier.
        __history (list[dict[str, str]]): Conversation history for chat mode.

    """

    def __init__(self) -> None:
        """Initialize the AIService with default model configurations."""
        self.__text_model: str = "deepseek-r1:8b"
        self.__image_model: str = "gemma3:27b"
        self.__ollama_keep_alive_single_query: int = 0
        self.__ollama_keep_alive_simple_query: str = "60s"
        self.__ollama_keep_alive_complex_query: str = "10m"
        self.__ollama_keep_alive_batch_query: str = "1h"
        self.__ollama_keep_alive_very_complex_task: int = -1
        self.__history: list[dict[str, str]] = []

    def ask(self, question: str) -> str:
        """Ask a question to the AI model and get a response.

        Args:
            question (str): The question to ask the AI model.

        Returns:
            str: The response from the AI model.

        """
        response: ChatResponse = chat(
            model=self.__text_model,
            messages=[{"role": "user", "content": question}],
            stream=False,
            think=True,
            keep_alive=self.__ollama_keep_alive_single_query,
        )

        return str(response.message.content)

    def chat(self, question: str) -> str:
        """Chat with the AI model maintaining conversation history.

        Args:
            question (str): The question to ask the AI model.

        Returns:
            str: The response from the AI model.

        """
        self.__history.append({"role": "user", "content": question})

        response: ChatResponse = chat(
            model=self.__text_model,
            messages=self.__history,
            stream=False,
            think=True,
            keep_alive=self.__ollama_keep_alive_complex_query,
        )

        self.__history.append(
            {"role": "assistant", "content": response.message.content}
        )

        return str(response.message.content)
