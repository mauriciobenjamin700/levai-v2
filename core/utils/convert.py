"""Utils module for converting audio files to WAV format for speech recognition."""

import os

from pydub import AudioSegment


def convert_audio_to_wav(audio_path: str) -> str:
    """Convert any audio format to WAV for speech recognition.

    Args:
        audio_path (str): Path to the original audio file

    Returns:
        str: Path to the converted WAV file

    """
    try:
        # Verificar se arquivo existe
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")

        # Detectar extensão do arquivo
        file_extension = os.path.splitext(audio_path)[1].lower()

        # Se já é WAV, verificar se é compatível
        if file_extension == ".wav":
            try:
                # Testar se o WAV é compatível
                audio = AudioSegment.from_wav(audio_path)
                # Se chegou aqui, o WAV é válido
                return audio_path
            except:
                print("Arquivo WAV não é compatível, convertendo...")

        # Carregar áudio baseado na extensão
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
            # Tentar carregamento genérico
            audio = AudioSegment.from_file(audio_path)

        # Converter para formato compatível com speech_recognition
        # Mono, 16kHz, 16-bit
        audio = audio.set_channels(1)  # Mono
        audio = audio.set_frame_rate(16000)  # 16kHz
        audio = audio.set_sample_width(2)  # 16-bit

        # Criar arquivo WAV temporário
        wav_path = os.path.splitext(audio_path)[0] + "_converted.wav"
        audio.export(wav_path, format="wav")

        return wav_path

    except Exception as e:
        raise Exception(f"Erro na conversão de áudio: {e}")
