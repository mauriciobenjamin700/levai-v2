"""Function to download a video using yt-dlp."""

import os
from os.path import abspath, dirname, join

from yt_dlp import YoutubeDL

from core.constants import TEMP_VIDEO_FILE_NAME

output_dir = abspath(join(dirname(abspath(__file__)), "temp"))
os.makedirs(output_dir, exist_ok=True)


def clean_temp_folder():
    """Remove todos os arquivos da pasta temp exceto arquivos .py."""
    temp_dir = join(dirname(abspath(__file__)), "temp")

    if not os.path.exists(temp_dir):
        return

    try:
        for file in os.listdir(temp_dir):
            file_path = join(temp_dir, file)
            # Apagar apenas arquivos (não pastas) que não sejam .py
            if os.path.isfile(file_path) and not file.endswith(".py"):
                os.remove(file_path)
                print(f"Arquivo removido: {file}")
    except Exception as e:
        print(f"Erro ao limpar pasta temp: {e}")


def get_first_non_py_file(folder_path: str) -> str:
    """Retorna o nome do primeiro arquivo que não seja .py na pasta.

    Args:
        folder_path (str): Caminho da pasta para procurar

    Returns:
        str: Nome do arquivo encontrado ou None se não encontrar

    """
    if not os.path.exists(folder_path):
        return None

    try:
        for file in os.listdir(folder_path):
            file_path = join(folder_path, file)
            # Verificar se é arquivo e não é .py
            if os.path.isfile(file_path) and not file.endswith(".py"):
                return file
        return None
    except Exception as e:
        print(f"Erro ao buscar arquivo: {e}")
        return None


def download_video_mp4(video_url: str) -> str | None:
    """Download a video from a given URL using yt-dlp.

    Args:
        video_url (str): The URL of the video to download.

    Returns:
        bool: True if the download was successful, False otherwise.

    """
    clean_temp_folder()

    if not os.access(output_dir, os.W_OK):
        print(f"Sem permissão de escrita em: {output_dir}")
        return None

    ydl_opts = {
        "outtmpl": join(output_dir, TEMP_VIDEO_FILE_NAME),
        "format": "best",
        "noplaylist": True,
        "keepvideo": True,  # Manter arquivo original se merge falhar
        "merge_output_format": "mp4",  # Forçar saída em MP4
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return get_first_non_py_file(output_dir)
    except Exception as e:
        print(f"Error: {e}")
        return False


def download_video_hd(video_url: str) -> str | None:
    """Download a video from a given URL using yt-dlp.

    Args:
        video_url (str): The URL of the video to download.

    Returns:
        bool: True if the download was successful, False otherwise.

    """
    try:

        clean_temp_folder()

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": join(output_dir, TEMP_VIDEO_FILE_NAME),
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return get_first_non_py_file(output_dir)

    except Exception as e:
        print("Error: ", e)
        return False
