import io
import os
import tempfile
import wave

import numpy as np
import pytest
from gtts import gTTS
from pydub import AudioSegment
from pydub.generators import Sine
from pypdf import PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


@pytest.fixture
def simple_pdf():
    """Single Page PDF fixture for testing."""
    # Criar PDF usando reportlab
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Adicionar conteúdo
    c.drawString(100, 750, "Este é um PDF de teste")
    c.drawString(100, 730, "Gerado para testes automatizados")
    c.drawString(100, 710, "Conteúdo em português para testar OCR")
    c.drawString(100, 690, "123456789 - números para validação")

    c.showPage()
    c.save()

    # Salvar em arquivo temporário
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        tmp_file.write(buffer.getvalue())
        pdf_path = tmp_file.name

    yield pdf_path

    # Cleanup
    if os.path.exists(pdf_path):
        os.remove(pdf_path)


@pytest.fixture
def multi_page_pdf():
    """Multiple page PDF fixture for testing."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Página 1
    c.drawString(100, 750, "Página 1 - Introdução")
    c.drawString(100, 730, "Este é um PDF de teste com múltiplas páginas")
    c.showPage()

    # Página 2
    c.drawString(100, 750, "Página 2 - Conteúdo")
    c.drawString(100, 730, "Mais conteúdo para testar extração")
    c.drawString(100, 710, "• Item de lista 1")
    c.drawString(100, 690, "• Item de lista 2")
    c.showPage()

    # Página 3
    c.drawString(100, 750, "Página 3 - Conclusão")
    c.drawString(100, 730, "Texto final do documento")
    c.showPage()

    c.save()

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        tmp_file.write(buffer.getvalue())
        pdf_path = tmp_file.name

    yield pdf_path

    if os.path.exists(pdf_path):
        os.remove(pdf_path)


@pytest.fixture
def empty_pdf():
    """Empty PDF fixture for testing."""
    writer = PdfWriter()

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        writer.write(tmp_file)
        pdf_path = tmp_file.name

    yield pdf_path

    if os.path.exists(pdf_path):
        os.remove(pdf_path)


@pytest.fixture
def complex_pdf():
    """Complex PDF fixture for testing with multiple sections."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        doc = SimpleDocTemplate(tmp_file.name)

        styles = getSampleStyleSheet()
        story = []

        # Título
        title = Paragraph("DOCUMENTO DE TESTE", styles["Title"])
        story.append(title)
        story.append(Spacer(1, 12))

        # Seções
        sections = [
            ("1. INTRODUÇÃO", "Este documento foi gerado automaticamente para testes."),
            (
                "2. METODOLOGIA",
                "Utilizamos pypdf e reportlab para criar PDFs de teste.",
            ),
            (
                "3. RESULTADOS",
                "Os testes devem conseguir extrair este texto corretamente.",
            ),
            ("4. CONCLUSÃO", "PDF gerado com sucesso para validação automática."),
        ]

        for section_title, section_content in sections:
            heading = Paragraph(section_title, styles["Heading2"])
            content = Paragraph(section_content, styles["Normal"])

            story.append(heading)
            story.append(Spacer(1, 6))
            story.append(content)
            story.append(Spacer(1, 12))

        doc.build(story)
        pdf_path = tmp_file.name

    yield pdf_path

    if os.path.exists(pdf_path):
        os.remove(pdf_path)


@pytest.fixture
def synthetic_audio_wav():
    """Cria áudio WAV sintético com texto falado simulado."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        # Parâmetros do áudio
        sample_rate = 16000  # 16kHz para speech recognition

        # Gerar tons que simulam fala (frequências de vogais)
        # Simular "Olá teste automatizado"
        frequencies = [
            (400, 0.3),  # "O" - som grave
            (800, 0.2),  # "lá" - som agudo
            (600, 0.3),  # "tes" - som médio
            (500, 0.3),  # "te" - som médio-grave
            (700, 0.4),  # "au" - som agudo
            (450, 0.3),  # "to" - som grave
            (550, 0.3),  # "ma" - som médio
            (650, 0.3),  # "ti" - som médio-agudo
            (500, 0.4),  # "za" - som médio-grave
            (400, 0.3),  # "do" - som grave
        ]

        # Gerar áudio sintético
        audio_data = np.array([])
        for freq, dur in frequencies:
            t = np.linspace(0, dur, int(sample_rate * dur), False)
            # Tom com envelope para soar mais natural
            envelope = np.exp(-t * 2)  # Decay exponencial
            tone = np.sin(freq * 2 * np.pi * t) * envelope * 0.3
            audio_data = np.concatenate([audio_data, tone])

            # Adicionar pausa entre "palavras"
            pause = np.zeros(int(sample_rate * 0.1))
            audio_data = np.concatenate([audio_data, pause])

        # Normalizar e converter para 16-bit
        audio_data = audio_data / np.max(np.abs(audio_data))
        audio_data = (audio_data * 32767).astype(np.int16)

        # Salvar como WAV
        with wave.open(tmp_file.name, "w") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())

        audio_path = tmp_file.name

    yield audio_path

    if os.path.exists(audio_path):
        os.remove(audio_path)


@pytest.fixture
def synthetic_speech_audio():
    """Cria áudio mais realista usando pydub com múltiplos tons."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        # Criar sequência de tons que simula "teste de áudio"
        audio = AudioSegment.empty()

        # Padrões de frequência para simular palavras
        word_patterns = [
            # "teste" - 4 sílabas com frequências variadas
            [(600, 200), (500, 150), (700, 200), (450, 200)],
            # pausa
            [(0, 200)],
            # "de" - 2 sílabas
            [(400, 150), (550, 200)],
            # pausa
            [(0, 200)],
            # "áudio" - 3 sílabas
            [(700, 200), (500, 150), (600, 250)],
        ]

        for word in word_patterns:
            for freq, duration in word:
                if freq == 0:
                    # Silêncio
                    tone = AudioSegment.silent(duration=duration)
                else:
                    # Tom com variação para soar mais natural
                    tone = Sine(freq).to_audio_segment(duration=duration)
                    # Aplicar fade in/out para suavizar
                    tone = tone.fade_in(20).fade_out(20)
                    # Reduzir volume
                    tone = tone - 20  # -20dB

                audio += tone

        # Converter para formato compatível com speech recognition
        audio = audio.set_channels(1)  # Mono
        audio = audio.set_frame_rate(16000)  # 16kHz

        # Exportar
        audio.export(tmp_file.name, format="wav")
        audio_path = tmp_file.name

    yield audio_path

    if os.path.exists(audio_path):
        os.remove(audio_path)


@pytest.fixture
def text_to_speech_audio():
    """Cria áudio usando TTS se disponível, senão usa sintético."""
    try:
        # Tentar usar gTTS (Google Text-to-Speech)
        text = "Este é um teste de extração de texto de áudio automatizado"

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tts = gTTS(text=text, lang="pt")
            tts.save(tmp_file.name)

            # Converter MP3 para WAV para compatibilidade
            audio = AudioSegment.from_mp3(tmp_file.name)
            wav_path = tmp_file.name.replace(".mp3", ".wav")
            audio.export(wav_path, format="wav")

            # Remover MP3 temporário
            os.remove(tmp_file.name)

            yield wav_path

            if os.path.exists(wav_path):
                os.remove(wav_path)

    except ImportError:
        # Fallback para áudio sintético se gTTS não estiver disponível
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            # Criar padrão de fala sintética mais complexo
            sample_rate = 16000

            # Simular "Este é um teste"
            sentence_pattern = [
                # "Este"
                [(400, 0.2), (600, 0.15), (500, 0.2), (450, 0.15)],
                # pausa
                [(0, 0.1)],
                # "é"
                [(550, 0.3)],
                # pausa
                [(0, 0.1)],
                # "um"
                [(400, 0.2), (500, 0.2)],
                # pausa
                [(0, 0.1)],
                # "teste"
                [(600, 0.2), (500, 0.15), (700, 0.2), (450, 0.2)],
            ]

            audio_data = np.array([])

            for word in sentence_pattern:
                for freq, duration in word:
                    if freq == 0:
                        # Silêncio
                        silence = np.zeros(int(sample_rate * duration))
                        audio_data = np.concatenate([audio_data, silence])
                    else:
                        # Gerar tom com modulação
                        t = np.linspace(0, duration, int(sample_rate * duration), False)

                        # Tom base com harmônicos
                        tone = np.sin(freq * 2 * np.pi * t)
                        tone += 0.3 * np.sin(
                            freq * 2 * 2 * np.pi * t
                        )  # Primeira harmônica
                        tone += 0.1 * np.sin(
                            freq * 3 * 2 * np.pi * t
                        )  # Segunda harmônica

                        # Aplicar envelope
                        envelope = np.exp(-t * 1.5) + 0.2
                        tone = tone * envelope * 0.2

                        audio_data = np.concatenate([audio_data, tone])

            # Normalizar e converter
            audio_data = audio_data / np.max(np.abs(audio_data))
            audio_data = (audio_data * 32767).astype(np.int16)

            # Salvar
            with wave.open(tmp_file.name, "w") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data.tobytes())

            audio_path = tmp_file.name

        yield audio_path

        if os.path.exists(audio_path):
            os.remove(audio_path)


@pytest.fixture
def multiple_audio_samples():
    """Cria múltiplos arquivos de áudio com diferentes características."""
    samples = {}

    # Áudio curto (1 segundo)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        audio = Sine(440).to_audio_segment(duration=1000)  # 1 segundo
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(tmp_file.name, format="wav")
        samples["short"] = tmp_file.name

    # Áudio médio (5 segundos) - simula frase
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        audio = AudioSegment.empty()
        # Padrão de fala: palavra + pausa + palavra + pausa
        for i in range(3):  # 3 "palavras"
            word = Sine(400 + i * 100).to_audio_segment(duration=800)
            pause = AudioSegment.silent(duration=300)
            audio += word + pause

        audio = audio.set_frame_rate(16000).set_channels(1) - 15  # -15dB
        audio.export(tmp_file.name, format="wav")
        samples["medium"] = tmp_file.name

    # Áudio longo (10 segundos) - simula parágrafo
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        audio = AudioSegment.empty()
        frequencies = [350, 400, 450, 500, 550, 600]  # Variação de tons

        for freq in frequencies:
            sentence = Sine(freq).to_audio_segment(duration=1200)
            sentence = sentence.fade_in(100).fade_out(100)
            pause = AudioSegment.silent(duration=400)
            audio += sentence + pause

        audio = audio.set_frame_rate(16000).set_channels(1) - 10  # -10dB
        audio.export(tmp_file.name, format="wav")
        samples["long"] = tmp_file.name

    yield samples

    # Cleanup
    for file_path in samples.values():
        if os.path.exists(file_path):
            os.remove(file_path)


@pytest.fixture
def noisy_audio():
    """Cria áudio com ruído para testar robustez."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        # Gerar sinal de fala
        speech = Sine(500).to_audio_segment(duration=2000)  # 2 segundos

        # Adicionar ruído branco
        noise = (
            AudioSegment.from_file("tests/fixtures/white_noise.wav")
            if os.path.exists("tests/fixtures/white_noise.wav")
            else AudioSegment.silent(duration=2000)
        )

        # Se não tem ruído, criar ruído sintético
        if len(noise) == 0:
            # Gerar ruído branco sintético
            sample_rate = 16000
            duration = 2.0
            noise_data = np.random.normal(0, 0.1, int(sample_rate * duration))
            noise_data = (noise_data * 32767).astype(np.int16)

            # Converter para AudioSegment
            noise = AudioSegment(
                noise_data.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1
            )

        # Mixar fala com ruído (fala mais alta que ruído)
        mixed = speech.overlay(noise - 25)  # Ruído 25dB mais baixo
        mixed = mixed.set_frame_rate(16000).set_channels(1)

        mixed.export(tmp_file.name, format="wav")
        audio_path = tmp_file.name

    yield audio_path

    if os.path.exists(audio_path):
        os.remove(audio_path)
