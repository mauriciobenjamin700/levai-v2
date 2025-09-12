    document.addEventListener('DOMContentLoaded', function() {
        const videoInput = document.getElementById('video');
        const videoPreview = document.getElementById('videoPreview');
        const previewVideo = document.getElementById('previewVideo');
        const videoInfo = document.getElementById('videoInfo');
        const convertBtn = document.getElementById('convertBtn');
        const clearBtn = document.getElementById('clearBtn');
        const loadingIndicator = document.getElementById('loadingIndicator');
        const convertForm = document.getElementById('convertForm');
        
        // Preview do vídeo
        videoInput.addEventListener('change', function() {
            const file = this.files[0];
            
            if (file) {
                // Mostrar preview
                const url = URL.createObjectURL(file);
                previewVideo.src = url;
                videoPreview.style.display = 'block';
                
                // Informações do arquivo
                const fileSizeMB = (file.size / 1024 / 1024).toFixed(2);
                const fileType = file.type || 'Desconhecido';
                videoInfo.innerHTML = `
                    <strong>📁 Nome:</strong> ${file.name}<br>
                    <strong>💾 Tamanho:</strong> ${fileSizeMB} MB<br>
                    <strong>🎭 Tipo:</strong> ${fileType}
                `;
                
                convertBtn.disabled = false;
            } else {
                videoPreview.style.display = 'none';
                convertBtn.disabled = true;
            }
        });
        
        // Botão limpar
        clearBtn.addEventListener('click', function() {
            videoInput.value = '';
            videoPreview.style.display = 'none';
            convertBtn.disabled = true;
            loadingIndicator.style.display = 'none';
            convertBtn.innerHTML = '🎬 Converter para MP4';
        });
        
        // Envio do formulário
        convertForm.addEventListener('submit', function(e) {
            if (!videoInput.files.length) {
                e.preventDefault();
                alert('Por favor, selecione um vídeo!');
                return;
            }
            
            // Mostrar indicador de carregamento
            loadingIndicator.style.display = 'block';
            convertBtn.disabled = true;
            convertBtn.innerHTML = '⏳ Convertendo...';
            
            // Esconder preview para economizar espaço
            videoPreview.style.display = 'none';
        });
    
    });