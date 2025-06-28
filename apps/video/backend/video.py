"""Function to download a video using yt-dlp."""

from os.path import abspath, dirname

from yt_dlp import YoutubeDL


def download_video(video_url: str) -> True:
    """Download a video from a given URL using yt-dlp.

    Args:
        video_url (str): The URL of the video to download.

    Returns:
        bool: True if the download was successful, False otherwise.

    """
    try:

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": f"{abspath(dirname(abspath(__file__)))}/video",
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return True

    except Exception as e:
        print("Error: ", e)
        return False
