"""Chat application views module."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from core.repositories import ChatRepository
from core.schemas import ChatResponse
from core.services.extract import ExtractService
from core.utils.enums import ChatRole, UploadDirs
from core.utils.upload import save_uploaded_file


@login_required
def chat_view(request: HttpRequest, chat_id: str = None) -> HttpResponse:
    """Render the chat view for authenticated users.

    Args:
        request (HttpRequest): The HTTP request object.
        chat_id (str, optional): The ID of the chat to display.

    Returns:
        HttpResponse: Rendered chat view.

    """
    if request.method == "POST":
        message = request.POST.get("message")
        document = request.FILES.get("document")
        audio = request.FILES.get("audio")
        image = request.FILES.get("image")
        video = request.FILES.get("video")

        print("MANDEI UM POST")
        print("CHAT ID DA LINHA 34", chat_id)
        if not chat_id:
            chat_id = request.POST.get("chat_id")

            print("CHAT ID DA LINHA 38", chat_id)

        # Validação
        if not message:
            messages.error(request, "A mensagem é obrigatória!")
            if chat_id:
                return redirect("chat_detail", chat_id=chat_id)
            return redirect("chat_view")

        try:

            if not chat_id:
                chat = ChatRepository.create_chat(user=request.user, title=message[:50])
                chat = ChatRepository.add_chat(chat)
                print("CHAT DA LINHA 56", chat)
            else:
                # Buscar chat existente
                chat = ChatRepository.get_chat(chat_id=chat_id)
                print("CHAT DA LINHA 59", chat)
                if not chat:
                    messages.error(request, "Chat não encontrado!")
                    return redirect("chat_view")

                # ✅ Verificar se pertence ao usuário
                if chat.user.id != request.user.id:
                    messages.error(request, "Acesso negado!")
                    return redirect("chat_view")

            metadata = {
                "document": None,
                "audio": None,
                "image": None,
                "video": None,
            }

            if document:
                document_path = save_uploaded_file(document, UploadDirs.DOCUMENTS)
                metadata["document"] = ExtractService.extract_text_from_pdf(
                    document_path
                )

            if image:
                image_path = save_uploaded_file(image, UploadDirs.IMAGES)
                metadata["image"] = ExtractService.extract_text_from_image(image_path)

            if video:
                video_path = save_uploaded_file(video, UploadDirs.VIDEOS)
                print(f"Vídeo salvo em: {video_path}")

            if audio:
                audio_path = save_uploaded_file(audio, UploadDirs.AUDIO)
                metadata["audio"] = ExtractService.transcribe_audio(audio_path)

            content: str = ""

            for key, value in metadata.items():
                if value:
                    content += f"{key.capitalize()}: {value}\n"

            content = message + content

            chat_message = ChatRepository.create_chat_message(
                chat=chat,
                role=ChatRole.USER,
                content=content,
            )

            chat_message = ChatRepository.add_chat_message(chat_message)

            messages.success(request, "Mensagem enviada com sucesso!")

            response: ChatResponse = ChatRepository.map_chat_to_response(chat)

            return redirect("chat_detail", chat_id=chat.id)

        except Exception as e:
            messages.error(request, f"Erro ao processar: {str(e)}")
            if chat_id:
                return redirect("chat_detail", chat_id=chat_id)
            return redirect("chat_view")

    elif request.method == "GET":
        if chat_id:
            print("GET DE CHAT COM ID: ", chat_id)
            try:
                chat = ChatRepository.get_chat(chat_id=chat_id)
                if not chat or chat.user.id != request.user.id:
                    messages.error(request, "Chat não encontrado!")
                    return redirect("chat_view")

                response = ChatRepository.map_chat_to_response(chat)
                return render(request, "chat_details.html", {"chat": response})

            except Exception as e:
                messages.error(request, f"Erro: {str(e)}")
                return redirect("chat_view")
        else:
            print("GET DE CHAT SEM ID")
            chats = ChatRepository.get_all_chats(user_id=request.user.id)
            response = []
            for chat in chats:
                response.append(ChatRepository.map_chat_to_response(chat))

            return render(request, "chat.html", {"chats": response})
