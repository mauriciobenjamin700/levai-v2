"""ExtractService module for extracting text from various file formats such as:

- PDF,
- images,
- audio files.
"""

import os
import re
import tempfile

import pytesseract
import speech_recognition as sr
from pdf2image import convert_from_path
from PIL import Image
from pydub import AudioSegment
from pypdf import PdfReader
from typing_extensions import Literal

from core.utils.convert import convert_audio_to_wav


class ExtractService:
    """Get text from various file formats such as.

    - PDF,
    - images,
    - and audio files.

    Methods:
        extract_text_from_pdf: Extract text from a PDF file.
        extract_text_from_pdf_ocr: Extract text from a PDF file using OCR.
        extract_text_from_image: Extract text from an image file using OCR.
        transcribe_audio: Method for audio transcription that tries different approaches
        clean_and_format_text: Clean and format raw text.

    """

    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extract text from a PDF file.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            str: Extracted text from the PDF file.

        """
        try:
            text = ""

            reader = PdfReader(pdf_path)

            for page in reader.pages:

                text += page.extract_text()

            return ExtractService.clean_and_format_text(text)

        except Exception as e:
            error = f"""
                Error on ExtractService in method extract_text_from_pdf
                Error: {e}
                """
            print(error)
            raise Exception(error)

    @staticmethod
    def extract_text_from_pdf_ocr(pdf_path: str) -> str:
        """Extract text from a PDF file using OCR (Optical Character Recognition).

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            str: Extracted text from the PDF file using OCR.

        """
        try:
            # Converter PDF para imagens
            images = convert_from_path(pdf_path)
            text = ""

            for image in images:
                # Usar OCR para extrair texto
                page_text = pytesseract.image_to_string(image, lang="por")
                text += page_text + "\n"

            return text.strip()
        except Exception as e:
            error = f"""
                Error on ExtractService in method extract_text_from_pdf_ocr
                Error: {e}
            """
            raise Exception(error)

    @staticmethod
    def extract_text_from_image(image_path: str) -> str:
        """Extract text from an image file using OCR (Optical Character Recognition).

        Args:
            image_path (str): The path to the image file.

        Returns:
            str: Extracted text from the image file.

        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang="por")
            return text.strip()
        except Exception as e:
            error = f"""
                Error on ExtractService in method extract_text_from_image
                Error: {e}
            """
            raise Exception(error)

    @staticmethod
    def transcribe_audio(audio_path: str) -> str:
        """Transcribe audio using Google Speech Recognition.

        Args:
            audio_path (str): Path to the audio file.

        Returns:
            str: Transcribed text from the audio file.

        """
        try:
            # Validar arquivo primeiro
            audio_info = ExtractService.__validate_audio_file(audio_path)

            # Se arquivo é muito grande, usar chunks
            if audio_info["size_mb"] > 25:  # > 25MB
                print("Arquivo grande detectado, usando transcrição por chunks...")
                return ExtractService.__transcribe_audio_with_chunks(audio_path)
            else:
                # Usar método normal
                return ExtractService.__transcribe_audio_google(audio_path)

        except Exception as e:
            raise Exception(f"Falha na transcrição robusta: {e}")

    @staticmethod
    def clean_and_format_text(text: str, mode: Literal["human", "ia"] = "human") -> str:
        """Clean and format raw text extracted from PDF or other sources.

        Args:
            text (str): Raw text to be cleaned and formatted
            mode (Literal["human", "ia"]): Mode of formatting

        Returns:
            str: Cleaned and formatted text

        """
        text = ExtractService.__clean_and_format_text(text)
        text = ExtractService.__format_pdf_text_advanced(text)

        if mode == "ia":
            text = ExtractService.__format_for_ai_context(text)

        return text

    @staticmethod
    def __clean_and_format_text(text: str) -> str:
        """Clean and format raw text extracted from PDF or other sources.

        Args:
            text (str): Raw text to be cleaned and formatted

        Returns:
            str: Cleaned and formatted text

        """
        if not text:
            return ""

        # Remover espaços múltiplos
        text = re.sub(r"\s+", " ", text)

        # Remover quebras de linha desnecessárias
        text = re.sub(r"\n\s*\n", "\n\n", text)

        # Corrigir espaçamento após pontuação
        text = re.sub(r"([.!?])\s*([A-Z])", r"\1 \2", text)

        # Remover espaços antes de pontuação
        text = re.sub(r"\s+([,.!?;:])", r"\1", text)

        # Adicionar espaço após pontuação se necessário
        text = re.sub(r"([,.!?;:])([A-Za-z])", r"\1 \2", text)

        # Corrigir quebras de palavra
        text = re.sub(r"(\w+)\s*\n\s*(\w+)", r"\1\2", text)

        # Limpar espaços no início e fim
        text = text.strip()

        return text

    @staticmethod
    def __format_pdf_text_advanced(text: str) -> str:
        """Advance formatting for PDF text to improve readability.

        Args:
            text (str): Raw text extracted from PDF

        Returns:
            str: Formatted text with improved structure

        """
        if not text:
            return ""

        # Remover hifenização no final de linha
        text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", text)

        # Juntar palavras quebradas por espaços
        text = re.sub(r"(\w)\s+(\w)\s+(\w)", r"\1\2\3", text)

        # Corrigir títulos e seções
        text = re.sub(r"\n([A-Z][A-Z\s]+)\n", r"\n\n**\1**\n\n", text)

        # Corrigir listas com bullets
        text = re.sub(r"\n\s*[●•]\s*", r"\n• ", text)
        text = re.sub(r"\n\s*○\s*", r"\n  ○ ", text)

        # Corrigir numeração
        text = re.sub(r"\n\s*(\d+)\.\s*", r"\n\1. ", text)

        # Corrigir parágrafos
        text = re.sub(r"([.!?])\s*\n\s*([A-Z])", r"\1\n\n\2", text)

        # Limpar múltiplas quebras de linha
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    @staticmethod
    def __extract_structured_content(text: str) -> dict:
        """Extract structured content from formatted text.

        Example:
            input:
            '''
            TÍTULO DO DOCUMENTO
            **Seção 1**
            Conteúdo da seção 1.
            **Seção 2**
            Conteúdo da seção 2.
            • Ponto importante 1
            • Ponto importante 2
            Parágrafo adicional com mais informações.
            **Seção 3**
            Conteúdo da seção 3.
            '''

            output:
            {
                "title": "TÍTULO DO DOCUMENTO",
                "sections": [
                    {"title": "Seção 1", "content": ["Conteúdo da seção 1."]},
                    {"title": "Seção 2", "content": ["Conteúdo da seção 2."]},
                    {"title": "Seção 3", "content": ["Conteúdo da seção 3."]}
                ],
                "lists": [
                    "• Ponto importante 1",
                    "• Ponto importante 2"
                ],
                "paragraphs": [
                    "Parágrafo adicional com mais informações."
                ]
            }

        Args:
            text (str): Formatted text to be structured

        Returns:
            dict: Structured content with title, sections, lists, and paragraphs

        """
        structure = {"title": "", "sections": [], "lists": [], "paragraphs": []}

        lines = text.split("\n")
        current_section = None
        current_paragraph = []

        for line in lines:
            line = line.strip()

            if not line:
                if current_paragraph:
                    structure["paragraphs"].append(" ".join(current_paragraph))
                    current_paragraph = []
                continue

            # Detectar título (primeira linha em maiúsculas)
            if not structure["title"] and line.isupper():
                structure["title"] = line

            # Detectar seções
            elif line.startswith("**") and line.endswith("**"):
                if current_paragraph:
                    structure["paragraphs"].append(" ".join(current_paragraph))
                    current_paragraph = []

                current_section = line.strip("*")
                structure["sections"].append({"title": current_section, "content": []})

            # Detectar listas
            elif (
                line.startswith("•")
                or line.startswith("○")
                or re.match(r"^\d+\.", line)
            ):
                structure["lists"].append(line)

            # Parágrafos normais
            else:
                current_paragraph.append(line)

        # Adicionar último parágrafo
        if current_paragraph:
            structure["paragraphs"].append(" ".join(current_paragraph))

        return structure

    @staticmethod
    def __format_for_ai_context(text: str, max_length: int = 4000) -> str:
        """Format text for AI context, ensuring it is concise and structured.

        Args:
            text (str): Raw text to be formatted
            max_length (int): Maximum length of the formatted text

        Returns:
            str: Formatted text suitable for AI context

        """
        # Estruturar conteúdo
        structure = ExtractService.__extract_structured_content(text)

        # Criar resumo estruturado
        result = []

        if structure["title"]:
            result.append(f"TÍTULO: {structure['title']}")
            result.append("")

        # Adicionar seções principais
        for section in structure["sections"][:3]:  # Primeiras 3 seções
            result.append(f"SEÇÃO: {section['title']}")
            result.append("")

        # Adicionar parágrafos mais relevantes
        for i, paragraph in enumerate(
            structure["paragraphs"][:5]
        ):  # Primeiros 5 parágrafos
            if len(paragraph) > 50:  # Apenas parágrafos substanciais
                result.append(f"Parágrafo {i+1}: {paragraph}")
                result.append("")

        # Adicionar listas se houver
        if structure["lists"]:
            result.append("PONTOS IMPORTANTES:")
            for item in structure["lists"][:10]:  # Primeiros 10 itens
                result.append(item)
            result.append("")

        final_text = "\n".join(result)

        # Truncar se necessário
        if len(final_text) > max_length:
            final_text = final_text[:max_length] + "..."

        return final_text

    @staticmethod
    def __validate_audio_file(audio_path: str) -> dict:
        """Validate and get information about the audio file.

        Args:
            audio_path (str): Path to the audio file

        Returns:
            dict: Audio file information

        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")

        file_size = os.path.getsize(audio_path)
        file_extension = os.path.splitext(audio_path)[1].lower()

        # Formatos suportados
        supported_formats = [
            ".wav",
            ".mp3",
            ".mp4",
            ".m4a",
            ".webm",
            ".ogg",
            ".flac",
            ".aac",
            ".wma",
            ".aiff",
        ]

        return {
            "path": audio_path,
            "size_mb": round(file_size / (1024 * 1024), 2),
            "extension": file_extension,
            "is_supported": file_extension in supported_formats,
            "filename": os.path.basename(audio_path),
        }

    @staticmethod
    def __transcribe_audio_google(audio_path: str) -> str:
        """Transcreve áudio usando Google Speech Recognition.

        Args:
            audio_path (str): Caminho do arquivo de áudio (qualquer formato)

        Returns:
            str: Texto transcrito

        """
        converted_file = None

        try:
            # Validar arquivo
            audio_info = ExtractService.__validate_audio_file(audio_path)

            if not audio_info["is_supported"]:
                raise ValueError(
                    f"Formato de áudio não suportado: {audio_info['extension']}"
                )

            if audio_info["size_mb"] > 100:  # Limite de 100MB
                raise ValueError(
                    f"Arquivo muito grande: {audio_info['size_mb']}MB (máximo: 100MB)"
                )

            # Converter para WAV se necessário
            wav_path = convert_audio_to_wav(audio_path)
            converted_file = wav_path if wav_path != audio_path else None

            # Configurar reconhecedor
            r = sr.Recognizer()

            # Processar áudio
            with sr.AudioFile(wav_path) as source:
                print("Ajustando para ruído ambiente...")
                r.adjust_for_ambient_noise(source, duration=1)

                print("Gravando áudio...")
                audio_data = r.record(source)

            print("Transcrevendo com Google Speech Recognition...")
            text = r.recognize_google(audio_data, language="pt-BR")

            if not text.strip():
                raise ValueError("Nenhum texto foi reconhecido no áudio")

            print(f"Transcrição concluída: {len(text)} caracteres")
            return text.strip()

        except sr.UnknownValueError:
            raise Exception("Google Speech Recognition não conseguiu entender o áudio.")
        except sr.RequestError as e:
            raise Exception(f"Erro no serviço Google Speech Recognition: {e}")
        except Exception as e:
            raise Exception(f"Erro na transcrição: {e}")
        finally:
            # Limpar arquivo convertido se foi criado
            if converted_file and os.path.exists(converted_file):
                try:
                    os.remove(converted_file)
                except:
                    pass

    @staticmethod
    def __transcribe_audio_with_chunks(
        audio_path: str, chunk_duration: int = 60
    ) -> str:
        """Transcreve áudios longos dividindo em chunks menores.

        Args:
            audio_path (str): Caminho do arquivo de áudio
            chunk_duration (int): Duração de cada chunk em segundos

        Returns:
            str: Texto transcrito completo

        """
        try:
            # Carregar áudio
            audio = AudioSegment.from_file(audio_path)

            # Se áudio é menor que chunk_duration, usar método normal
            if len(audio) <= chunk_duration * 1000:  # converter para ms
                return ExtractService.__transcribe_audio_google(audio_path)

            # Dividir em chunks
            chunks = []
            for i in range(0, len(audio), chunk_duration * 1000):
                chunk = audio[i : i + chunk_duration * 1000]
                chunks.append(chunk)

            # Transcrever cada chunk
            full_transcription = []

            for i, chunk in enumerate(chunks):
                print(f"Processando chunk {i+1}/{len(chunks)}...")

                # Salvar chunk temporário
                with tempfile.NamedTemporaryFile(
                    suffix=".wav", delete=False
                ) as tmp_file:
                    chunk.export(tmp_file.name, format="wav")
                    chunk_path = tmp_file.name

                try:
                    # Transcrever chunk
                    chunk_text = ExtractService.__transcribe_audio_google(chunk_path)
                    if chunk_text.strip():
                        full_transcription.append(chunk_text.strip())
                except Exception as e:
                    print(f"Erro no chunk {i+1}: {e}")
                    continue
                finally:
                    # Limpar arquivo temporário
                    if os.path.exists(chunk_path):
                        os.remove(chunk_path)

            # Juntar transcrições
            result = " ".join(full_transcription)

            if not result.strip():
                raise Exception("Nenhum texto foi transcrito de nenhum chunk")

            return result

        except Exception as e:
            raise Exception(f"Erro na transcrição por chunks: {e}")
