"""Chat application views module."""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from apps.chat.models import ChatMessage
from core.repositories import ChatRepository
from core.schemas.chat import ChatResponse


@login_required
def chat_view(request: HttpRequest) -> HttpResponse:
    """Render the chat view for authenticated users.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered chat view.

    """
    if request.method == "POST":
        content = request.POST.get("content")
        if content and request.user.is_authenticated:
            model = ChatRepository.create_chat(user_id=request.user.id)
            model = ChatRepository.add_chat(model)
        return redirect("chat")  # ou use reverse_lazy

    chats = ChatRepository.get_all_chats(user_id=request.user.id)

    response:list[ChatResponse] = []

    for chat in chats:
        response.append(
            ChatRepository.map_chat_to_response(chat)
        )


    return render(request, "chat.html", {"chats": response})
