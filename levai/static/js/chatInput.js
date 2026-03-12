document.addEventListener("DOMContentLoaded", function() {
    var mediaRecorder;
    var recordedChunks = [];
    var recordedBlob = null;

    function refreshIcons() {
        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }
    }

    // Botoes de selecao de arquivo
    document.getElementById("search-button").addEventListener("click", function() {
        document.getElementById("document").click();
    });

    document.getElementById("image-button").addEventListener("click", function() {
        document.getElementById("image").click();
    });

    document.getElementById("video-button").addEventListener("click", function() {
        document.getElementById("video").click();
    });

    document.getElementById("upload-audio-button").addEventListener("click", function() {
        document.getElementById("audio").click();
    });

    // Botao de gravar audio
    document.getElementById("record-button").addEventListener("click", function() {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            stopRecording();
        } else {
            startRecording();
        }
    });

    // Botoes de remover
    document.getElementById("deleteRecording").addEventListener("click", function() {
        deleteRecording();
    });

    document.getElementById("deleteImage").addEventListener("click", function() {
        deleteImage();
    });

    document.getElementById("deleteVideo").addEventListener("click", function() {
        deleteVideo();
    });

    // Event listeners para arquivos

    // Documento
    document.getElementById("document").addEventListener("change", function() {
        var indicator = document.getElementById("documentIndicator");
        if (this.files.length > 0) {
            indicator.style.display = "inline";
            indicator.textContent = this.files[0].name;
        } else {
            indicator.style.display = "none";
        }
    });

    // Imagem
    document.getElementById("image").addEventListener("change", function() {
        var indicator = document.getElementById("imageIndicator");
        var preview = document.getElementById("imagePreview");
        var img = document.getElementById("previewImg");

        if (this.files.length > 0) {
            var file = this.files[0];
            indicator.style.display = "inline";
            indicator.textContent = file.name;

            var reader = new FileReader();
            reader.onload = function(e) {
                img.src = e.target.result;
                preview.style.display = "block";
            };
            reader.readAsDataURL(file);
        } else {
            indicator.style.display = "none";
            preview.style.display = "none";
        }
    });

    // Video
    document.getElementById("video").addEventListener("change", function() {
        var indicator = document.getElementById("videoIndicator");
        var preview = document.getElementById("videoPreview");
        var video = document.getElementById("previewVideo");

        if (this.files.length > 0) {
            var file = this.files[0];
            indicator.style.display = "inline";
            indicator.textContent = file.name;

            var url = URL.createObjectURL(file);
            video.src = url;
            preview.style.display = "block";
        } else {
            indicator.style.display = "none";
            preview.style.display = "none";
        }
    });

    // Audio
    document.getElementById("audio").addEventListener("change", function() {
        var indicator = document.getElementById("audioIndicator");
        if (this.files.length > 0) {
            indicator.style.display = "inline";
            indicator.textContent = this.files[0].name;
            deleteRecording();
        } else {
            indicator.style.display = "none";
        }
    });

    // Funcoes de gravacao de audio
    function startRecording() {
        navigator.mediaDevices.getUserMedia({ audio: true }).then(function(stream) {
            mediaRecorder = new MediaRecorder(stream);
            recordedChunks = [];

            mediaRecorder.ondataavailable = function(event) {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = function() {
                recordedBlob = new Blob(recordedChunks, { type: "audio/wav" });

                var audioPlayer = document.getElementById("recordedAudio");
                audioPlayer.src = URL.createObjectURL(recordedBlob);
                document.getElementById("audioPlayer").style.display = "block";

                document.getElementById("recordingIndicator").style.display = "none";
                document.getElementById("audioIndicator").style.display = "inline";
                document.getElementById("audioIndicator").textContent = "Audio gravado";

                stream.getTracks().forEach(function(track) { track.stop(); });
            };

            mediaRecorder.start();

            var btn = document.getElementById("record-button");
            btn.innerHTML = '<i data-lucide="square"></i>';
            btn.title = "Parar gravacao";
            refreshIcons();
            document.getElementById("recordingIndicator").style.display = "inline";

        }).catch(function(error) {
            LevAI.toast("Erro ao acessar microfone: " + error.message, "error");
        });
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
            var btn = document.getElementById("record-button");
            btn.innerHTML = '<i data-lucide="mic"></i>';
            btn.title = "Gravar audio";
            refreshIcons();
        }
    }

    // Funcoes de remocao
    function deleteRecording() {
        recordedBlob = null;
        document.getElementById("audioPlayer").style.display = "none";
        document.getElementById("audioIndicator").style.display = "none";
        document.getElementById("recordingIndicator").style.display = "none";
        document.getElementById("audio").value = "";
    }

    function deleteImage() {
        document.getElementById("image").value = "";
        document.getElementById("imagePreview").style.display = "none";
        document.getElementById("imageIndicator").style.display = "none";
    }

    function deleteVideo() {
        document.getElementById("video").value = "";
        document.getElementById("videoPreview").style.display = "none";
        document.getElementById("videoIndicator").style.display = "none";
    }

    // Validacao e envio do formulario
    document.getElementById("chatForm").addEventListener("submit", function(e) {
        var message = document.getElementById("search").value.trim();

        if (!message) {
            e.preventDefault();
            LevAI.toast("Por favor, digite uma mensagem!", "warning");
            return false;
        }

        // Se ha audio gravado, criar arquivo e adicionar ao form
        if (recordedBlob) {
            var file = new File([recordedBlob], "recorded_audio.wav", { type: "audio/wav" });
            var dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            document.getElementById("audio").files = dataTransfer.files;
        }

        // Loading state
        var sendButton = document.getElementById("send-button");
        if (sendButton) {
            sendButton.disabled = true;
            sendButton.innerHTML = '<i data-lucide="loader" class="spin"></i>';
            sendButton.setAttribute("title", "Enviando...");
            refreshIcons();
        }
    });
});
