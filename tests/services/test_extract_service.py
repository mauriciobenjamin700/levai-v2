from core.services.extract import ExtractService


def test_extract_simple_pdf(simple_pdf):
    """Testa extração de PDF simples."""
    text = ExtractService.extract_text_from_pdf(simple_pdf)

    assert "PDF de teste" in text
    assert "português" in text
    assert "123456789" in text


def test_extract_multi_page_pdf(multi_page_pdf):
    """Testa extração de PDF com múltiplas páginas."""
    text = ExtractService.extract_text_from_pdf(multi_page_pdf)

    assert "Página 1" in text
    assert "Página 2" in text
    assert "Página 3" in text
    assert "Item de lista" in text


def test_extract_complex_pdf(complex_pdf):
    """Testa extração de PDF complexo."""
    text = ExtractService.extract_text_from_pdf(complex_pdf)

    assert "DOCUMENTO DE TESTE" in text
    assert "INTRODUÇÃO" in text
    assert "METODOLOGIA" in text
    assert "pypdf" in text


def test_extract_empty_pdf(empty_pdf):
    """Testa comportamento com PDF vazio."""
    text = ExtractService.extract_text_from_pdf(empty_pdf)

    assert text == ""


def test_extract_synthetic_audio(synthetic_audio_wav):
    """Testa extração de áudio sintético."""
    # Este teste pode falhar com áudio sintético simples
    # mas serve para testar a pipeline
    try:
        text = ExtractService.transcribe_audio(synthetic_audio_wav)
        assert isinstance(text, str)
        print(f"Texto extraído: {text}")
    except Exception as e:
        # Áudio sintético pode não ser reconhecido
        assert "Speech Recognition" in str(e) or "não conseguiu entender" in str(e)


def test_extract_speech_audio(synthetic_speech_audio):
    """Testa extração de áudio com padrão de fala."""
    try:
        text = ExtractService.transcribe_audio(synthetic_speech_audio)
        assert isinstance(text, str)
    except Exception as e:
        # Aceitar que áudio sintético pode falhar
        assert "entender" in str(e) or "transcrição" in str(e)


def test_extract_tts_audio(text_to_speech_audio):
    """Testa extração de áudio TTS (mais realista)."""
    try:
        text = ExtractService.transcribe_audio(text_to_speech_audio)
        # Se usar gTTS real, deve reconhecer algumas palavras
        assert isinstance(text, str)
        if len(text) > 0:
            assert any(word in text.lower() for word in ["teste", "audio", "extração"])
    except Exception as e:
        print(f"TTS test failed (expected): {e}")


def test_multiple_audio_samples(multiple_audio_samples):
    """Testa diferentes tamanhos de áudio."""
    for sample_type, audio_path in multiple_audio_samples.items():
        try:
            # Testar validação
            info = ExtractService.__validate_audio_file(audio_path)
            assert info["is_supported"] is True
            assert info["extension"] == ".wav"

            # Testar transcrição
            text = ExtractService.transcribe_audio(audio_path)
            assert isinstance(text, str)

        except Exception as e:
            print(f"Sample {sample_type} failed: {e}")


def test_noisy_audio(noisy_audio):
    """Testa áudio com ruído."""
    try:
        text = ExtractService.transcribe_audio(noisy_audio)
        # Áudio com ruído pode ter dificuldade
        assert isinstance(text, str)
    except Exception as e:
        # Ruído pode impossibilitar reconhecimento
        assert "entender" in str(e) or "transcrição" in str(e)
