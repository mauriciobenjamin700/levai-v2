"""Task controller module for calendar view and CRUD operations."""

import calendar
import logging
from datetime import date, time

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from levai.core.repositories.task import TaskRepository

logger: logging.Logger = logging.getLogger(__name__)

MONTH_NAMES: list[str] = [
    "",
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]


class TaskController:
    """Controller for task-related operations."""

    @staticmethod
    def get_calendar_view(request: HttpRequest) -> HttpResponse:
        """Render the calendar view with tasks for the requested month.

        Args:
            request (HttpRequest): The HTTP request object. Accepts
                optional query params 'year' and 'month'.

        Returns:
            HttpResponse: Rendered calendar view.

        """
        today: date = date.today()
        year: int = int(request.GET.get("year", today.year))
        month: int = int(request.GET.get("month", today.month))

        if month < 1:
            month = 12
            year -= 1
        elif month > 12:
            month = 1
            year += 1

        prev_month: int = month - 1 if month > 1 else 12
        prev_year: int = year if month > 1 else year - 1
        next_month: int = month + 1 if month < 12 else 1
        next_year: int = year if month < 12 else year + 1

        calendar.setfirstweekday(6)
        cal: list[list[int]] = calendar.monthcalendar(year, month)

        tasks = TaskRepository.get_tasks_for_month(
            request.user.id,
            year,
            month,
        )

        tasks_by_day: dict[int, list[object]] = {}
        for task in tasks:
            day: int = task.date.day
            if day not in tasks_by_day:
                tasks_by_day[day] = []
            tasks_by_day[day].append(
                TaskRepository.map_task_to_response(task),
            )

        weeks: list[list[dict[str, object]]] = []
        for week in cal:
            week_cells: list[dict[str, object]] = []
            for day in week:
                cell: dict[str, object] = {
                    "day": day,
                    "tasks": (tasks_by_day.get(day, []) if day != 0 else []),
                }
                week_cells.append(cell)
            weeks.append(week_cells)

        is_current_month: bool = year == today.year and month == today.month

        context: dict[str, object] = {
            "year": year,
            "month": month,
            "month_name": MONTH_NAMES[month],
            "weeks": weeks,
            "today_day": today.day if is_current_month else None,
            "prev_year": prev_year,
            "prev_month": prev_month,
            "next_year": next_year,
            "next_month": next_month,
            "tasks_list": [TaskRepository.map_task_to_response(t) for t in tasks],
        }

        return render(request, "task.html", context)

    @staticmethod
    def create_task(request: HttpRequest) -> HttpResponse:
        """Create a new task from POST data and redirect to calendar.

        Args:
            request (HttpRequest): The HTTP request object with
                POST data containing task fields.

        Returns:
            HttpResponse: Redirect to the calendar view.

        """
        try:
            title: str = request.POST.get("title", "")
            description: str = request.POST.get("description", "")
            task_date_str: str = request.POST.get("date", "")
            task_time_str: str = request.POST.get("time", "")
            priority: str = request.POST.get("priority", "medium")
            status: str = request.POST.get("status", "pending")

            task_date: date = date.fromisoformat(task_date_str)
            task_time: time | None = None
            if task_time_str:
                parts: list[str] = task_time_str.split(":")
                task_time = time(int(parts[0]), int(parts[1]))

            task = TaskRepository.create_task(
                user=request.user,
                title=title,
                task_date=task_date,
                task_time=task_time,
                description=description,
                priority=priority,
                status=status,
            )
            TaskRepository.add_task(task)

            return redirect(f"/task/?year={task_date.year}" f"&month={task_date.month}")

        except Exception as e:
            logger.error("Erro ao criar tarefa: %s", str(e))
            return redirect("task_view")

    @staticmethod
    def update_task(
        request: HttpRequest,
        task_id: str,
    ) -> HttpResponse:
        """Update an existing task from POST data.

        Args:
            request (HttpRequest): The HTTP request object with
                POST data containing updated task fields.
            task_id (str): The ID of the task to update.

        Returns:
            HttpResponse: Redirect to the calendar view.

        """
        try:
            task = TaskRepository.get_task(task_id)

            if str(task.user_id) != str(request.user.id):
                return redirect("task_view")

            task.title = request.POST.get("title", task.title)
            task.description = request.POST.get(
                "description",
                task.description,
            )

            task_date_str: str = request.POST.get("date", "")
            if task_date_str:
                task.date = date.fromisoformat(task_date_str)

            task_time_str: str = request.POST.get("time", "")
            if task_time_str:
                parts: list[str] = task_time_str.split(":")
                task.time = time(int(parts[0]), int(parts[1]))
            else:
                task.time = None

            task.priority = request.POST.get(
                "priority",
                task.priority,
            )
            task.status = request.POST.get("status", task.status)

            TaskRepository.update_task(task)

            return redirect(f"/task/?year={task.date.year}" f"&month={task.date.month}")

        except Exception as e:
            logger.error("Erro ao atualizar tarefa: %s", str(e))
            return redirect("task_view")

    @staticmethod
    def delete_task(
        request: HttpRequest,
        task_id: str,
    ) -> HttpResponse:
        """Delete a task and redirect to calendar.

        Args:
            request (HttpRequest): The HTTP request object.
            task_id (str): The ID of the task to delete.

        Returns:
            HttpResponse: Redirect to the calendar view.

        """
        try:
            task = TaskRepository.get_task(task_id)

            if str(task.user_id) != str(request.user.id):
                return redirect("task_view")

            year: int = task.date.year
            month: int = task.date.month
            TaskRepository.delete_task(task_id)

            return redirect(f"/task/?year={year}&month={month}")

        except Exception as e:
            logger.error("Erro ao excluir tarefa: %s", str(e))
            return redirect("task_view")

    @staticmethod
    def get_task_json(
        request: HttpRequest,
        task_id: str,
    ) -> JsonResponse:
        """Return a task as JSON for the edit modal.

        Args:
            request (HttpRequest): The HTTP request object.
            task_id (str): The ID of the task to retrieve.

        Returns:
            JsonResponse: The task data as JSON.

        """
        try:
            task = TaskRepository.get_task(task_id)

            if str(task.user_id) != str(request.user.id):
                return JsonResponse(
                    {"error": "Não autorizado"},
                    status=403,
                )

            return JsonResponse(
                {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "date": task.date.isoformat(),
                    "time": (task.time.strftime("%H:%M") if task.time else ""),
                    "priority": task.priority,
                    "status": task.status,
                }
            )

        except Exception as e:
            logger.error("Erro ao buscar tarefa: %s", str(e))
            return JsonResponse(
                {"error": "Tarefa não encontrada"},
                status=404,
            )
