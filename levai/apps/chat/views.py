"""Chat application views module."""

from typing import Optional

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from levai.apps.chat.controller import ChatController


@login_required
def chat_view(request: HttpRequest, chat_id: Optional[str] = None) -> HttpResponse:
    """Render the chat view for authenticated users.

    Args:
        request (HttpRequest): The HTTP request object.
        chat_id (str, optional): The ID of the chat to display.

    Returns:
        HttpResponse: Rendered chat view.

    """
    print("=" * 50)
    print(f"🔍 REQUEST METHOD: {request.method}")
    print(f"🔍 CHAT_ID RECEBIDO: '{chat_id}'")  # 🔄 Aspas para ver string vazia
    print(f"🔍 CHAT_ID IS NONE: {chat_id is None}")  # 🔄 Verificar se é None
    print(f"🔍 CHAT_ID IS EMPTY: {chat_id == ''}")  # 🔄 Verificar se é string vazia
    print(f"🔍 TIPO DO CHAT_ID: {type(chat_id)}")
    print(f"🔍 URL COMPLETA: {request.get_full_path()}")
    print("=" * 50)
    try:
        if request.method == "POST":

            return ChatController.new_chat_view(request, chat_id)

        elif request.method == "GET":
            return ChatController.get_chat_view(request, chat_id)

        else:
            return HttpResponse("Método não permitido", status=405)

    except Exception as e:
        print(f"Erro ao processar a requisição: {str(e)}")
        return HttpResponse("Erro interno do servidor", status=500)


def test_chat_detail(request: HttpRequest, chat_id: str) -> HttpResponse:
    """View de teste para diagnóstico."""
    return HttpResponse(f"Chat ID: {chat_id}, Tipo: {type(chat_id)}")
