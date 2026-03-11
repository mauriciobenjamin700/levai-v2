"""Chat application views module."""

import logging
from typing import Optional

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from levai.apps.chat.controller import ChatController

logger = logging.getLogger(__name__)


@login_required
def chat_view(request: HttpRequest, chat_id: Optional[str] = None) -> HttpResponse:
    """Render the chat view for authenticated users.

    Args:
        request (HttpRequest): The HTTP request object.
        chat_id (str, optional): The ID of the chat to display.

    Returns:
        HttpResponse: Rendered chat view.

    """
    try:
        if request.method == "POST":
            return ChatController.new_chat_view(request, chat_id)

        elif request.method == "GET":
            return ChatController.get_chat_view(request, chat_id)

        else:
            return HttpResponse("Metodo nao permitido", status=405)

    except Exception as e:
        logger.error("Erro ao processar a requisicao: %s", str(e))
        return HttpResponse("Erro interno do servidor", status=500)
