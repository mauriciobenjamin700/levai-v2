import os
from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip


def convert_to_mp4_moviepy(
    input_path: str, output_path: str = None, bitrate: str = "2000k"
) -> str:
    """Converte vídeo para MP4 usando MoviePy.

    Args:
        input_path (str): Caminho do vídeo de entrada
        output_path (str): Caminho de saída
        bitrate (str): Bitrate do vídeo (ex: '1000k', '2000k')

    Returns:
        str: Caminho do MP4 gerado

    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

    # Gerar nome de saída se não fornecido
    if output_path is None:
        video_name = Path(input_path).stem
        output_dir = Path(input_path).parent
        output_path = str(output_dir / f"{video_name}.mp4")

    try:
        # Carregar vídeo
        video_clip = VideoFileClip(input_path)

        # Converter para MP4
        video_clip.write_videofile(
            output_path, codec="libx264", bitrate=bitrate, audio_codec="aac"
        )

        # Fechar clip para liberar memória
        video_clip.close()

        print(f"Vídeo convertido: {output_path}")
        return output_path

    except Exception as e:
        raise Exception(f"Erro na conversão: {e}")


def mov_to_mp4_moviepy(mov_path: str, output_path: str = None) -> str:
    """Converts MOV para MP4 usando MoviePy."""
    return convert_to_mp4_moviepy(mov_path, output_path)
