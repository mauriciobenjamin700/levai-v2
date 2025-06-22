"""User service module."""

from django.contrib.auth import login, logout
from django.http import HttpRequest

from core import messages
from core.repositories import UserRepository
from core.schemas import UserRequest, UserResponse
from core.schemas.user import UserLogin


class UserService:
    """Service for managing user-related operations.

    Methods:
        add_user
            Add a new user to the database.
        get_user
            Retrieve a user by ID, username, or email.
        update_user
            Update an existing user in the database.
        delete_user
            Delete a user by ID.

    """

    @staticmethod
    def add_user(request: UserRequest) -> UserResponse:
        """Add a new user to the database.

        Args:
            request (UserRequest): The user request model containing user data.

        Returns:
            UserResponse: The user response model containing the added user data.

        """
        model = UserRepository.map_request_to_model(request)

        model = UserRepository.add_user(model)

        response = UserRepository.map_model_to_response(model)

        return response

    @staticmethod
    def get_user_by_id(user_id: str) -> UserResponse:
        """Retrieve a user by ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            UserResponse: User data if found, otherwise raises an error.

        """
        model = UserRepository.get_user(user_id=user_id)

        if model is None:

            raise ValueError(messages.ERROR_USER_NOT_FOUND)

        response = UserRepository.map_model_to_response(model)

        return response

    @staticmethod
    def get_user_by_email(email: str) -> UserResponse:
        """Retrieve a user by email.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            UserResponse: User data if found, otherwise raises an error.

        """
        model = UserRepository.get_user(email=email)

        if model is None:

            raise ValueError(messages.ERROR_USER_NOT_FOUND)

        response = UserRepository.map_model_to_response(model)

        return response

    @staticmethod
    def update_user(request: UserRequest, user_id: str) -> UserResponse:
        """Update an existing user in the database.

        Args:
            request (UserRequest): The user request model containing updated user data.
            user_id (str): The ID of the user to update.

        Returns:
            UserResponse: The user response model containing the updated user data.

        """
        model = UserRepository.get_user(user_id=user_id)

        if model is None:
            raise ValueError(messages.ERROR_USER_NOT_FOUND)

        for key, value in request.to_dict().items():
            if value is not None and hasattr(model, key):
                setattr(model, key, value)

        model = UserRepository.update_user(model)

        response = UserRepository.map_model_to_response(model)

        return response

    @staticmethod
    def delete_user(user_id: str) -> bool:
        """Delete a user by ID.

        Args:
            user_id (str): The ID of the user to delete.

        Returns:
            bool: True if the user was deleted successfully, False otherwise.

        """
        return UserRepository.delete_user(user_id)

    @staticmethod
    def login(request: HttpRequest, login_request: UserLogin) -> bool:
        """Log in a user.

        Args:
            request (HttpRequest): The HTTP request object.
            login_request (UserLogin): Containing email and password.

        Returns:
            Bool: True if the login was successful, False otherwise.

        """
        user = UserRepository.get_user(email=login_request.email)

        if not user:
            raise ValueError(messages.ERROR_USER_NOT_FOUND)

        if not user.check_password(login_request.password):

            raise ValueError(messages.ERROR_USER_LOGIN)

        if user:
            login(request, user)
            return True

        return False

    @staticmethod
    def logout(request: HttpRequest) -> bool:
        """Log out a user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            bool: True if the logout was successful, False otherwise.

        """
        if request.user.is_authenticated:
            logout(request)
            return True

        return False
