document.addEventListener('DOMContentLoaded', function() {
    const videoInput = document.getElementById('video');
    const videoPreview = document.getElementById('videoPreview');
    const previewVideo = document.getElementById('previewVideo');
    const videoInfo = document.getElementById('videoInfo');
    const convertBtn = document.getElementById('convertBtn');
    const clearBtn = document.getElementById('clearBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const videoForm = document.getElementById('videoForm');
    
    // Preview do vídeo quando selecionado
    videoInput.addEventListener('change', function() {
        const file = this.files[0];
        
        if (file) {
            // Mostrar preview
            const url = URL.createObjectURL(file);
            previewVideo.src = url;
            videoPreview.style.display = 'block';
            
            // Mostrar informações do arquivo
            const fileSizeMB = (file.size / 1024 / 1024).toFixed(2);
            videoInfo.textContent = `📁 ${file.name} - 💾 ${fileSizeMB} MB`;
            
            // Habilitar botão de conversão
            convertBtn.disabled = false;
        } else {
            // Esconder preview
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
    });
    
    // Envio do formulário
    videoForm.addEventListener('submit', function(e) {
        if (!videoInput.files.length) {
            e.preventDefault();
            alert('Por favor, selecione um vídeo!');
            return;
        }
        
        // Mostrar indicador de carregamento
        loadingIndicator.style.display = 'block';
        convertBtn.disabled = true;
        convertBtn.textContent = '⏳ Convertendo...';
        
        // O formulário será enviado normalmente
    });
    
    // Verificar se há mensagens de erro para esconder loading
});