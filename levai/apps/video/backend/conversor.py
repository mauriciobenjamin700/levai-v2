"""Video format conversion module using MoviePy."""

import os
from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip


def convert_to_mp4_moviepy(
    input_path: str, output_path: str | None = None, bitrate: str = "2000k"
) -> str:
    """Convert a video file to MP4 format using MoviePy.

    Args:
        input_path (str): Path to the input video file.
        output_path (str | None): Path for the output MP4 file.
            If None, generates a path based on the input filename.
        bitrate (str): Video bitrate (e.g., "1000k", "2000k").

    Returns:
        str: Path to the generated MP4 file.

    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: If the conversion fails.

    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

    if output_path is None:
        video_name: str = Path(input_path).stem
        output_dir: Path = Path(input_path).parent
        output_path = str(output_dir / f"{video_name}.mp4")

    try:
        video_clip: VideoFileClip = VideoFileClip(input_path)

        video_clip.write_videofile(
            output_path, codec="libx264", bitrate=bitrate, audio_codec="aac"
        )

        video_clip.close()

        print(f"Vídeo convertido: {output_path}")
        return output_path

    except Exception as e:
        raise Exception(f"Erro na conversão: {e}")


def mov_to_mp4_moviepy(mov_path: str, output_path: str | None = None) -> str:
    """Convert a MOV file to MP4 format using MoviePy.

    Args:
        mov_path (str): Path to the input MOV file.
        output_path (str | None): Path for the output MP4 file.

    Returns:
        str: Path to the generated MP4 file.

    """
    return convert_to_mp4_moviepy(mov_path, output_path)
