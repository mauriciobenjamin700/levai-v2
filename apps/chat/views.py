"""Chat application views module."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from core.repositories import ChatRepository
from core.schemas.chat import ChatResponse
from core.utils.enums import UploadDirs
from core.utils.upload import save_uploaded_file


@login_required
def chat_view(request: HttpRequest) -> HttpResponse:
    """Render the chat view for authenticated users.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered chat view.

    """
    if request.method == "POST":
        message = request.POST.get("message")
        document = request.FILES.get("document")
        audio = request.FILES.get("audio")
        image = request.FILES.get("image")
        video = request.FILES.get("video")

        # Validação
        if not message:
            messages.error(request, "A mensagem é obrigatória!")
            return redirect("chat_view")

        # Processar os dados
        try:

            if document:
                document_path = save_uploaded_file(document, UploadDirs.DOCUMENTS)
                print(f"Documento salvo em: {document_path}")

            if image:
                image_path = save_uploaded_file(image, UploadDirs.IMAGES)
                print(f"Imagem salva em: {image_path}")

            if video:
                video_path = save_uploaded_file(video, UploadDirs.VIDEOS)
                print(f"Vídeo salvo em: {video_path}")

            if audio:
                audio_path = save_uploaded_file(audio, UploadDirs.AUDIO)
                print(f"Áudio salvo em: {audio_path}")

            chat = ChatRepository.create_chat(user_id=request.user.id, message=message)

            messages.success(request, "Mensagem enviada com sucesso!")

            chats = ChatRepository.get_all_chats(user_id=request.user.id)
            response: list[ChatResponse] = []
            for chat in chats:
                response.append(ChatRepository.map_chat_to_response(chat))

            return render(request, "chat.html", {"chats": response})

        except Exception as e:
            messages.error(request, f"Erro ao processar: {str(e)}")
            # ✅ Adicionar return aqui
            return redirect("chat_view")

    elif request.method == "GET":

        chats = ChatRepository.get_all_chats(user_id=request.user.id)

        response: list[ChatResponse] = []

        for chat in chats:
            response.append(ChatRepository.map_chat_to_response(chat))

        return render(request, "chat.html", {"chats": response})
