"""Task repository for database operations."""

from datetime import date, time

from levai.apps.task.models import Task
from levai.apps.user.models import User
from levai.core.schemas.task import TaskResponse


class TaskRepository:
    """Repository for managing task database operations."""

    @staticmethod
    def create_task(
        user: User,
        title: str,
        task_date: date,
        task_time: time | None = None,
        description: str = "",
        priority: str = "medium",
        status: str = "pending",
    ) -> Task:
        """Create a new task instance without saving to database.

        Args:
            user (User): The user who owns the task.
            title (str): The task title.
            task_date (date): The date for the task.
            task_time (time | None): Optional time for the task.
            description (str): Optional task description.
            priority (str): Priority level (low, medium, high).
            status (str): Task status (pending, in_progress, done).

        Returns:
            Task: The created task instance (not yet saved).

        """
        return Task(
            user=user,
            title=title,
            date=task_date,
            time=task_time,
            description=description,
            priority=priority,
            status=status,
        )

    @staticmethod
    def add_task(model: Task) -> Task:
        """Validate and save a task to the database.

        Args:
            model (Task): The task model instance to save.

        Returns:
            Task: The saved task instance.

        """
        model.full_clean()
        model.save()
        return model

    @staticmethod
    def get_task(task_id: str) -> Task:
        """Retrieve a task by its ID.

        Args:
            task_id (str): The ID of the task to retrieve.

        Returns:
            Task: The task instance.

        Raises:
            Task.DoesNotExist: If the task is not found.

        """
        return Task.objects.get(id=task_id)

    @staticmethod
    def get_tasks_for_month(user_id: str, year: int, month: int) -> list[Task]:
        """Retrieve all tasks for a given user in a specific month.

        Args:
            user_id (str): The ID of the user.
            year (int): The year to filter by.
            month (int): The month to filter by.

        Returns:
            list[Task]: List of tasks ordered by date and time.

        """
        return list(
            Task.objects.filter(
                user_id=user_id,
                date__year=year,
                date__month=month,
            ).order_by("date", "time")
        )

    @staticmethod
    def update_task(model: Task) -> Task:
        """Validate and update an existing task.

        Args:
            model (Task): The task model instance to update.

        Returns:
            Task: The updated task instance.

        """
        model.full_clean()
        model.save()
        return model

    @staticmethod
    def delete_task(task_id: str) -> bool:
        """Delete a task by its ID.

        Args:
            task_id (str): The ID of the task to delete.

        Returns:
            bool: True if the task was deleted successfully.

        Raises:
            Task.DoesNotExist: If the task is not found.

        """
        task = Task.objects.get(id=task_id)
        task.delete()
        return True

    @staticmethod
    def map_task_to_response(model: Task) -> TaskResponse:
        """Map a Task model instance to a TaskResponse schema.

        Args:
            model (Task): The task model instance.

        Returns:
            TaskResponse: The mapped task response schema.

        """
        return TaskResponse(
            id=str(model.id),
            user_id=str(model.user_id),
            title=model.title,
            description=model.description,
            date=model.date,
            time=model.time,
            priority=model.priority,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
