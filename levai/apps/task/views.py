"""Task application views module."""

import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse

from levai.apps.task.controller import TaskController

logger = logging.getLogger(__name__)


@login_required
def task_view(request: HttpRequest) -> HttpResponse:
    """Render the calendar view for authenticated users.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered calendar view.

    """
    try:
        return TaskController.get_calendar_view(request)
    except Exception as e:
        logger.error("Erro ao processar a requisicao: %s", str(e))
        return HttpResponse("Erro interno do servidor", status=500)


@login_required
def task_create_view(request: HttpRequest) -> HttpResponse:
    """Handle task creation via POST.

    Args:
        request (HttpRequest): The HTTP request object with POST data.

    Returns:
        HttpResponse: Redirect to the calendar view.

    """
    if request.method != "POST":
        return HttpResponse("Metodo nao permitido", status=405)

    try:
        return TaskController.create_task(request)
    except Exception as e:
        logger.error("Erro ao criar tarefa: %s", str(e))
        return HttpResponse("Erro interno do servidor", status=500)


@login_required
def task_detail_json_view(request: HttpRequest, task_id: str) -> JsonResponse:
    """Return task data as JSON for the edit modal.

    Args:
        request (HttpRequest): The HTTP request object.
        task_id (str): The ID of the task to retrieve.

    Returns:
        JsonResponse: The task data as JSON.

    """
    try:
        return TaskController.get_task_json(request, task_id)
    except Exception as e:
        logger.error("Erro ao buscar tarefa: %s", str(e))
        return JsonResponse({"error": "Erro interno"}, status=500)


@login_required
def task_update_view(request: HttpRequest, task_id: str) -> HttpResponse:
    """Handle task update via POST.

    Args:
        request (HttpRequest): The HTTP request object with POST data.
        task_id (str): The ID of the task to update.

    Returns:
        HttpResponse: Redirect to the calendar view.

    """
    if request.method != "POST":
        return HttpResponse("Metodo nao permitido", status=405)

    try:
        return TaskController.update_task(request, task_id)
    except Exception as e:
        logger.error("Erro ao atualizar tarefa: %s", str(e))
        return HttpResponse("Erro interno do servidor", status=500)


@login_required
def task_delete_view(request: HttpRequest, task_id: str) -> HttpResponse:
    """Handle task deletion via POST.

    Args:
        request (HttpRequest): The HTTP request object.
        task_id (str): The ID of the task to delete.

    Returns:
        HttpResponse: Redirect to the calendar view.

    """
    if request.method != "POST":
        return HttpResponse("Metodo nao permitido", status=405)

    try:
        return TaskController.delete_task(request, task_id)
    except Exception as e:
        logger.error("Erro ao excluir tarefa: %s", str(e))
        return HttpResponse("Erro interno do servidor", status=500)
