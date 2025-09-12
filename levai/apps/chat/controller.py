from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from levai.core.repositories.chat import ChatRepository
from levai.core.schemas.chat import ChatResponse
from levai.core.services.extract import ExtractService
from levai.core.utils.enums import ChatRole, UploadDirs
from levai.core.utils.upload import save_uploaded_file


class ChatController:
    """Controller for chat-related operations."""

    @staticmethod
    def get_chat_view(request: HttpRequest, chat_id: str | None = None) -> HttpResponse:
        """Render the chat view for authenticated users.

        Args:
            request (HttpRequest): The HTTP request object.
            chat_id (str | None): The ID of the chat to display.

        Returns:
            HttpResponse: Rendered chat view.

        """
        if chat_id:
            try:
                chat = ChatRepository.get_chat(chat_id=chat_id)
                if not chat or str(chat.user.id) != str(request.user.id):
                    print("CHAT NÃO ENCONTRADO OU NÃO PERTENCE AO USUÁRIO")
                    return redirect("chat_view")

                chat: ChatResponse = ChatRepository.map_chat_to_response(chat)
                return render(request, "chat_details.html", {"chat": chat})

            except Exception as e:
                print(f"Erro ao buscar o chat: {str(e)}")
                return redirect("chat_view")
        else:
            chats = ChatRepository.get_all_chats(user_id=request.user.id)
            response: list[ChatResponse] = []
            for chat in chats:
                response.append(ChatRepository.map_chat_to_response(chat))

            return render(request, "chat.html", {"chats": response})

    @staticmethod
    def new_chat_view(request: HttpRequest, chat_id: str | None = None) -> HttpResponse:
        """Handle the creation of a new chat or processing a message in
        an existing chat.

        Args:
            request (HttpRequest): The HTTP request object.
            chat_id (str | None): The ID of the chat to process.

        Returns:
            HttpResponse: Redirect to the chat detail view or the chat list.

        """
        try:
            message = request.POST.get("message")
            document = request.FILES.get("document")
            audio = request.FILES.get("audio")
            image = request.FILES.get("image")
            video = request.FILES.get("video")

            if not chat_id:
                chat_id = request.POST.get("chat_id")

            if not message:
                message = ""
            if not chat_id:
                chat = ChatRepository.create_chat(user=request.user, title=message[:50])
                chat = ChatRepository.add_chat(chat)
            else:
                chat = ChatRepository.get_chat(chat_id=chat_id)

                if chat.user.id != request.user.id:
                    print("CHAT NÃO PERTENCE AO USUÁRIO")
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

            ChatRepository.map_chat_to_response(chat)

            return redirect("chat_detail", chat_id=str(chat.id))

        except Exception as e:
            print(f"Erro ao processar a mensagem: {str(e)}")
            if chat_id:
                return redirect("chat_detail", chat_id=chat_id)
            return redirect("chat_view")
