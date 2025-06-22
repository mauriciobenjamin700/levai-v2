"""Contains the error and success messages for user operations."""

from .error import ERROR_USER_ALREADY_EXISTS, ERROR_USER_LOGIN, ERROR_USER_NOT_FOUND
from .handle import handle_error_message, handle_success_message

__all__ = [
    "handle_error_message",
    "handle_success_message",
    "ERROR_USER_NOT_FOUND",
    "ERROR_USER_ALREADY_EXISTS",
    "ERROR_USER_LOGIN",
]
