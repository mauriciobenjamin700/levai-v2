"""Task schemas for request and response validation."""

from datetime import date, datetime, time
from typing import Optional

from levai.core.schemas.base import BaseSchema


class TaskRequest(BaseSchema):
    """Schema for task creation and update requests.

    Attributes:
        title (str): The task title.
        description (str): Optional task description.
        date (date): The date the task is scheduled for.
        time (time | None): Optional time for the task.
        priority (str): Priority level (low, medium, high).
        status (str): Task status (pending, in_progress, done).

    """

    title: str
    description: str = ""
    date: date
    time: Optional[time] = None
    priority: str = "medium"
    status: str = "pending"


class TaskResponse(BaseSchema):
    """Schema for task response serialization.

    Attributes:
        id (str): The task unique identifier.
        user_id (str): The owner user identifier.
        title (str): The task title.
        description (str): The task description.
        date (date): The date the task is scheduled for.
        time (time | None): Optional time for the task.
        priority (str): Priority level.
        status (str): Task status.
        created_at (datetime): When the task was created.
        updated_at (datetime): When the task was last updated.

    """

    id: str
    user_id: str
    title: str
    description: str
    date: date
    time: Optional[time]
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime
