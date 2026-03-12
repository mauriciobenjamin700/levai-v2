"""Base schema for all Pydantic models in the application."""

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema for all Pydantic models in the application.

    Provides shared configuration and utility methods for
    serialization and deserialization of Pydantic models.

    """

    model_config = ConfigDict(use_enum_values=True, from_attributes=True)

    def to_dict(
        self,
        exclude: list[str] | None = None,
        include: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Convert the Pydantic model instance to a dictionary.

        Args:
            exclude (list[str] | None): List of fields to exclude from
                the dictionary. Defaults to None.
            include (dict[str, object] | None): Additional key-value pairs
                to merge into the dictionary. Defaults to None.

        Returns:
            dict[str, object]: Dictionary representation of the model.

        """
        if exclude is None:
            exclude = []

        data: dict[str, object] = {
            key: value
            for key, value in self.model_dump(exclude_none=True).items()
            if key not in exclude
        }

        if include:
            data.update(include)

        return data

    def from_object(self, obj: object) -> "BaseSchema":
        """Populate the Pydantic model instance from an object.

        Args:
            obj (object): The object to populate the Pydantic model
                instance from.

        Returns:
            BaseSchema: The populated Pydantic model instance.

        """
        return self.model_validate(obj)
