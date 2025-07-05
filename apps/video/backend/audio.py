import os
from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip


def video_to_mp3_moviepy(video_path: str, output_path: str = None) -> str:
    """Converte vídeo para MP3 usando MoviePy.

    Args:
        video_path (str): Caminho do arquivo de vídeo
        output_path (str): Caminho de saída (opcional)

    Returns:
        str: Caminho do arquivo MP3

    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {video_path}")

    # Gerar nome de saída se não fornecido
    if output_path is None:
        video_name = Path(video_path).stem
        output_dir = Path(video_path).parent
        output_path = str(output_dir / f"{video_name}.mp3")

    try:
        # Carregar vídeo e extrair áudio
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio

        # Salvar como MP3
        audio_clip.write_audiofile(output_path)

        # Fechar clips para liberar memória
        audio_clip.close()
        video_clip.close()

        print(f"Áudio extraído: {output_path}")
        return output_path

    except Exception as e:
        raise Exception(f"Erro na conversão: {e}")


def batch_video_to_mp3(video_folder: str, output_folder: str = None) -> list:
    """Converte todos os vídeos de uma pasta para MP3.

    Args:
        video_folder (str): Pasta com vídeos
        output_folder (str): Pasta de saída

    Returns:
        list: Lista com caminhos dos arquivos MP3 gerados

    """
    if output_folder is None:
        output_folder = video_folder

    os.makedirs(output_folder, exist_ok=True)

    video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"]
    converted_files = []

    for file in os.listdir(video_folder):
        if any(file.lower().endswith(ext) for ext in video_extensions):
            video_path = os.path.join(video_folder, file)
            try:
                mp3_path = video_to_mp3_moviepy(
                    video_path, os.path.join(output_folder, f"{Path(file).stem}.mp3")
                )
                converted_files.append(mp3_path)
            except Exception as e:
                print(f"Erro ao converter {file}: {e}")

    return converted_files
