from yt_dlp import YoutubeDL


def download_video(video_url: str, output_dir: str, file_name: str) -> None:

    # Configurações para o download
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Melhor qualidade de vídeo e áudio
        'outtmpl': f'{output_dir}/{file_name}',         # Nome e diretório do arquivo
    }

    # Realizar o download
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print("Download concluído!")
