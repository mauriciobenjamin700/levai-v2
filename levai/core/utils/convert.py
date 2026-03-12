"""Utils module for converting audio files to WAV format for speech recognition."""

import os

from pydub import AudioSegment


def convert_audio_to_wav(audio_path: str) -> str:
    """Convert any supported audio format to WAV for speech recognition.

    Converts the input audio to mono, 16kHz, 16-bit WAV format
    compatible with speech recognition engines.

    Args:
        audio_path (str): Path to the original audio file.

    Returns:
        str: Path to the converted WAV file, or the original path
            if it was already a compatible WAV.

    Raises:
        FileNotFoundError: If the audio file does not exist.
        Exception: If the conversion fails.

    """
    try:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        file_extension: str = os.path.splitext(audio_path)[1].lower()

        if file_extension == ".wav":
            try:
                audio: AudioSegment = AudioSegment.from_wav(audio_path)
                return audio_path
            except Exception:
                print("WAV file is not compatible, converting...")

        if file_extension == ".mp3":
            audio = AudioSegment.from_mp3(audio_path)
        elif file_extension in [".mp4", ".m4a"]:
            audio = AudioSegment.from_file(audio_path, format="mp4")
        elif file_extension == ".webm":
            audio = AudioSegment.from_file(audio_path, format="webm")
        elif file_extension == ".ogg":
            audio = AudioSegment.from_ogg(audio_path)
        elif file_extension == ".flac":
            audio = AudioSegment.from_file(audio_path, format="flac")
        elif file_extension == ".aac":
            audio = AudioSegment.from_file(audio_path, format="aac")
        elif file_extension == ".wma":
            audio = AudioSegment.from_file(audio_path, format="wma")
        else:
            audio = AudioSegment.from_file(audio_path)

        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_sample_width(2)

        wav_path: str = os.path.splitext(audio_path)[0] + "_converted.wav"
        audio.export(wav_path, format="wav")

        return wav_path

    except Exception as e:
        raise Exception(f"Audio conversion error: {e}")
