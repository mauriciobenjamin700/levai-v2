"""Models for the task application."""

from uuid import uuid4

from django.db import models

from levai.apps.user.models import User


class Task(models.Model):
    """Model to store user tasks.

    Attributes:
        id (UUID): Unique identifier for the task.
        user (User): Foreign key to the User model, representing the task owner.
        title (str): Title of the task.
        description (str): Optional description of the task.
        date (date): The date the task is scheduled for.
        time (time): Optional time for the task.
        priority (str): Priority level (low, medium, high).
        status (str): Task status (pending, in_progress, done).
        created_at (datetime): Timestamp when the task was created.
        updated_at (datetime): Timestamp when the task was last updated.

    """

    PRIORITY_CHOICES = [
        ("low", "Baixa"),
        ("medium", "Média"),
        ("high", "Alta"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("in_progress", "Em Progresso"),
        ("done", "Concluída"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Task model."""

        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["date", "time"]

    def __str__(self) -> str:
        """String representation of the Task instance.

        Returns:
            str: The task title and date.

        """
        return f"{self.title} ({self.date})"
