"""Audio extraction module for converting video files to MP3."""

import os
from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip


def video_to_mp3_moviepy(video_path: str, output_path: str | None = None) -> str:
    """Convert a video file to MP3 audio using MoviePy.

    Args:
        video_path (str): Path to the input video file.
        output_path (str | None): Path for the output MP3 file.
            If None, generates a path based on the input filename.

    Returns:
        str: Path to the generated MP3 file.

    Raises:
        FileNotFoundError: If the video file does not exist.
        Exception: If the conversion fails.

    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {video_path}")

    if output_path is None:
        video_name: str = Path(video_path).stem
        output_dir: Path = Path(video_path).parent
        output_path = str(output_dir / f"{video_name}.mp3")

    try:
        video_clip: VideoFileClip = VideoFileClip(video_path)
        audio_clip = video_clip.audio

        audio_clip.write_audiofile(output_path)

        audio_clip.close()
        video_clip.close()

        print(f"Áudio extraído: {output_path}")
        return output_path

    except Exception as e:
        raise Exception(f"Erro na conversão: {e}")


def batch_video_to_mp3(
    video_folder: str, output_folder: str | None = None
) -> list[str]:
    """Convert all video files in a folder to MP3.

    Args:
        video_folder (str): Path to the folder containing videos.
        output_folder (str | None): Path to the output folder.
            If None, uses the same folder as input.

    Returns:
        list[str]: List of paths to the generated MP3 files.

    """
    if output_folder is None:
        output_folder = video_folder

    os.makedirs(output_folder, exist_ok=True)

    video_extensions: list[str] = [
        ".mp4",
        ".avi",
        ".mkv",
        ".mov",
        ".wmv",
        ".flv",
    ]
    converted_files: list[str] = []

    for file in os.listdir(video_folder):
        if any(file.lower().endswith(ext) for ext in video_extensions):
            video_path: str = os.path.join(video_folder, file)
            try:
                mp3_path: str = video_to_mp3_moviepy(
                    video_path,
                    os.path.join(output_folder, f"{Path(file).stem}.mp3"),
                )
                converted_files.append(mp3_path)
            except Exception as e:
                print(f"Erro ao converter {file}: {e}")

    return converted_files
