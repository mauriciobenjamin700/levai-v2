"""Video download module using yt-dlp."""

import os
from os.path import abspath, dirname, join

from yt_dlp import YoutubeDL

from levai.core.constants import TEMP_VIDEO_FILE_NAME

output_dir: str = abspath(join(dirname(abspath(__file__)), "temp"))
os.makedirs(output_dir, exist_ok=True)


def clean_temp_folder() -> None:
    """Remove all non-Python files from the temp folder.

    Cleans up temporary files generated during video downloads
    while preserving any Python files in the directory.

    """
    temp_dir: str = join(dirname(abspath(__file__)), "temp")

    if not os.path.exists(temp_dir):
        return

    try:
        for file in os.listdir(temp_dir):
            file_path: str = join(temp_dir, file)
            if os.path.isfile(file_path) and not file.endswith(".py"):
                os.remove(file_path)
                print(f"Arquivo removido: {file}")
    except Exception as e:
        print(f"Erro ao limpar pasta temp: {e}")


def get_first_non_py_file(folder_path: str) -> str | None:
    """Return the name of the first non-Python file in a folder.

    Args:
        folder_path (str): Path to the folder to search.

    Returns:
        str | None: Name of the first non-Python file found,
            or None if no such file exists.

    """
    if not os.path.exists(folder_path):
        return None

    try:
        for file in os.listdir(folder_path):
            file_path: str = join(folder_path, file)
            if os.path.isfile(file_path) and not file.endswith(".py"):
                return file
        return None
    except Exception as e:
        print(f"Erro ao buscar arquivo: {e}")
        return None


def download_video_mp4(video_url: str) -> str | None:
    """Download a video in MP4 format from a given URL.

    Args:
        video_url (str): The URL of the video to download.

    Returns:
        str | None: Filename of the downloaded video,
            or None if the download failed.

    """
    clean_temp_folder()

    if not os.access(output_dir, os.W_OK):
        print(f"Sem permissão de escrita em: {output_dir}")
        return None

    ydl_opts: dict[str, object] = {
        "outtmpl": join(output_dir, TEMP_VIDEO_FILE_NAME),
        "format": "best",
        "noplaylist": True,
        "keepvideo": True,
        "merge_output_format": "mp4",
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return get_first_non_py_file(output_dir)
    except Exception as e:
        print(f"Error: {e}")
        return None


def download_video_hd(video_url: str) -> str | None:
    """Download a video in HD quality from a given URL.

    Args:
        video_url (str): The URL of the video to download.

    Returns:
        str | None: Filename of the downloaded video,
            or None if the download failed.

    """
    try:

        clean_temp_folder()

        ydl_opts: dict[str, object] = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": join(output_dir, TEMP_VIDEO_FILE_NAME),
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return get_first_non_py_file(output_dir)

    except Exception as e:
        print("Error: ", e)
        return None
