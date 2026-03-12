"""Models for the user app."""

from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model that extends the default Django user model.

    Attributes:
        id (str) : Unique identifier for the user.
        first_name (str) : First name of the user.
        last_name (str) : Last name of the user.
        username (str) : Unique username for the user.
        email (str) : Email address of the user.
        password (str) : Password for the user account.
        is_active (bool) : Indicates if the user account is active.
        is_staff (bool) : Indicates if the user can access the admin site.
        is_superuser (bool) : Indicates if the user has all permissions
        data_joined (datetime) : Date and time when the user joined.
        last_login (datetime) : Date and time of the user's last login.

    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the User model."""

        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        """Return a string representation of the user instance.

        Returns:
            str: Comma-separated key-value pairs of the user data.

        """
        return " ,".join([f"{key}: {value}" for key, value in self.to_dict().items()])

    def to_dict(
        self,
        exclude: list[str] | None = None,
        include: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Convert the user instance to a dictionary.

        Args:
            exclude (list[str] | None): List of fields to exclude.
                Defaults to None.
            include (dict[str, object] | None): Additional key-value pairs
                to merge into the dictionary. Defaults to None.

        Returns:
            dict[str, object]: Dictionary representation of the user instance.

        """
        if exclude is None:
            exclude = []

        data: dict[str, object] = {
            "id": str(self.id) if hasattr(self, "id") else None,
            "username": self.username,
            "email": self.email,
            "name": f"{self.first_name} {self.last_name}".strip(),
            "is_active": self.is_active,
            "is_staff": self.is_staff,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        for field in exclude:
            data.pop(field, None)

        if include:
            data.update(include)

        return data
