from ollama import ChatResponse, chat


class AIService:
    """
    AI services for handling text and image models using Ollama.

    Methods:
        ask(question: str) -> str: Ask a question to the AI model and get a response.
    
    """
    def __init__(self):
        self.__text_model = "deepseek-r1:8b"
        self.__image_model = "gemma3:27b"
        self.__ollama_keep_alive_single_query = 0
        self.__ollama_keep_alive_simple_query = "60s"
        self.__ollama_keep_alive_complex_query = "10m"
        self.__ollama_keep_alive_batch_query = "1h"
        self.__ollama_keep_alive_very_complex_task = -1
        self.__history = []

    def ask(self, question: str) -> str:
        """
        Ask a question to the AI model and get a response.

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
            keep_alive=self.__ollama_keep_alive_single_query
        )

        return response.message.content
    
    def chat(self, question: str) -> str:
        """
        Chat with the AI model and get a response.

        Args:
            question (str): The question to ask the AI model.

        Returns:
            str: The response from the AI model.
        """

        self.__history.append({
                "role": "user", 
                "content": question
            })

        response: ChatResponse = chat(
            model=self.__text_model,
            messages=self.__history,
            stream=False,
            think=True,
            keep_alive=self.__ollama_keep_alive_complex_query
        )

        self.__history.append({
            "role": "assistant", 
            "content": response.message.content
        })

        return response.message.content