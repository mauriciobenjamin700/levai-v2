document.addEventListener('DOMContentLoaded', function() {
    let mediaRecorder;
    let recordedChunks = [];
    let recordedBlob = null;
    
    // Botões de seleção de arquivo
    document.getElementById('search-button').addEventListener('click', function() {
        document.getElementById('document').click();
    });
    
    document.getElementById('image-button').addEventListener('click', function() {
        document.getElementById('image').click();
    });
    
    document.getElementById('video-button').addEventListener('click', function() {
        document.getElementById('video').click();
    });
    
    document.getElementById('upload-audio-button').addEventListener('click', function() {
        document.getElementById('audio').click();
    });
    
    // Botão de gravar áudio
    document.getElementById('record-button').addEventListener('click', function() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            stopRecording();
        } else {
            startRecording();
        }
    });
    
    // Botões de remover
    document.getElementById('deleteRecording').addEventListener('click', function() {
        deleteRecording();
    });
    
    document.getElementById('deleteImage').addEventListener('click', function() {
        deleteImage();
    });
    
    document.getElementById('deleteVideo').addEventListener('click', function() {
        deleteVideo();
    });
    
    // Event listeners para arquivos
    
    // Documento
    document.getElementById('document').addEventListener('change', function() {
        const indicator = document.getElementById('documentIndicator');
        if (this.files.length > 0) {
            indicator.style.display = 'inline';
            indicator.textContent = `📄 ${this.files[0].name}`;
        } else {
            indicator.style.display = 'none';
        }
    });
    
    // Imagem
    document.getElementById('image').addEventListener('change', function() {
        const indicator = document.getElementById('imageIndicator');
        const preview = document.getElementById('imagePreview');
        const img = document.getElementById('previewImg');
        
        if (this.files.length > 0) {
            const file = this.files[0];
            indicator.style.display = 'inline';
            indicator.textContent = `🖼️ ${file.name}`;
            
            // Mostrar preview
            const reader = new FileReader();
            reader.onload = function(e) {
                img.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            indicator.style.display = 'none';
            preview.style.display = 'none';
        }
    });
    
    // Vídeo
    document.getElementById('video').addEventListener('change', function() {
        const indicator = document.getElementById('videoIndicator');
        const preview = document.getElementById('videoPreview');
        const video = document.getElementById('previewVideo');
        
        if (this.files.length > 0) {
            const file = this.files[0];
            indicator.style.display = 'inline';
            indicator.textContent = `🎬 ${file.name}`;
            
            // Mostrar preview
            const url = URL.createObjectURL(file);
            video.src = url;
            preview.style.display = 'block';
        } else {
            indicator.style.display = 'none';
            preview.style.display = 'none';
        }
    });
    
    // Áudio
    document.getElementById('audio').addEventListener('change', function() {
        const indicator = document.getElementById('audioIndicator');
        if (this.files.length > 0) {
            indicator.style.display = 'inline';
            indicator.textContent = `🎵 ${this.files[0].name}`;
            deleteRecording(); // Limpar gravação se houver
        } else {
            indicator.style.display = 'none';
        }
    });
    
    // Funções de gravação de áudio (mantidas do código anterior)
    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            recordedChunks = [];
            
            mediaRecorder.ondataavailable = function(event) {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = function() {
                recordedBlob = new Blob(recordedChunks, { type: 'audio/wav' });
                
                const audioPlayer = document.getElementById('recordedAudio');
                audioPlayer.src = URL.createObjectURL(recordedBlob);
                document.getElementById('audioPlayer').style.display = 'block';
                
                document.getElementById('recordingIndicator').style.display = 'none';
                document.getElementById('audioIndicator').style.display = 'inline';
                document.getElementById('audioIndicator').textContent = '🎤 Áudio gravado';
                
                stream.getTracks().forEach(track => track.stop());
            };
            
            mediaRecorder.start();
            
            document.getElementById('record-button').innerHTML = '⏹️';
            document.getElementById('record-button').title = 'Parar gravação';
            document.getElementById('recordingIndicator').style.display = 'inline';
            
        } catch (error) {
            alert('Erro ao acessar microfone: ' + error.message);
        }
    }
    
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            document.getElementById('record-button').innerHTML = '🎤';
            document.getElementById('record-button').title = 'Gravar áudio';
        }
    }
    
    // Funções de remoção
    function deleteRecording() {
        recordedBlob = null;
        document.getElementById('audioPlayer').style.display = 'none';
        document.getElementById('audioIndicator').style.display = 'none';
        document.getElementById('recordingIndicator').style.display = 'none';
        document.getElementById('audio').value = '';
    }
    
    function deleteImage() {
        document.getElementById('image').value = '';
        document.getElementById('imagePreview').style.display = 'none';
        document.getElementById('imageIndicator').style.display = 'none';
    }
    
    function deleteVideo() {
        document.getElementById('video').value = '';
        document.getElementById('videoPreview').style.display = 'none';
        document.getElementById('videoIndicator').style.display = 'none';
    }
    
    // Validacao e envio do formulario
    document.getElementById('chatForm').addEventListener('submit', function(e) {
        const message = document.getElementById('search').value.trim();

        if (!message) {
            e.preventDefault();
            alert('Por favor, digite uma mensagem!');
            return false;
        }

        // Se ha audio gravado, criar arquivo e adicionar ao form
        if (recordedBlob) {
            const file = new File([recordedBlob], 'recorded_audio.wav', { type: 'audio/wav' });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            document.getElementById('audio').files = dataTransfer.files;
        }

        // Loading state - desabilitar botao e mostrar feedback
        const sendButton = document.getElementById('send-button');
        if (sendButton) {
            sendButton.disabled = true;
            sendButton.textContent = '...';
            sendButton.setAttribute('title', 'Enviando...');
        }
    });
});