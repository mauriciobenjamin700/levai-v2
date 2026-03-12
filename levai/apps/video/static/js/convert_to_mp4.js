document.addEventListener("DOMContentLoaded", function() {
    var videoInput = document.getElementById("video");
    var videoPreview = document.getElementById("videoPreview");
    var previewVideo = document.getElementById("previewVideo");
    var videoInfo = document.getElementById("videoInfo");
    var convertBtn = document.getElementById("convertBtn");
    var clearBtn = document.getElementById("clearBtn");
    var loadingIndicator = document.getElementById("loadingIndicator");
    var convertForm = document.getElementById("convertForm");

    videoInput.addEventListener("change", function() {
        var file = this.files[0];

        if (file) {
            var url = URL.createObjectURL(file);
            previewVideo.src = url;
            videoPreview.style.display = "block";

            var fileSizeMB = (file.size / 1024 / 1024).toFixed(2);
            var fileType = file.type || "Desconhecido";
            videoInfo.innerHTML =
                "<strong>Nome:</strong> " + file.name + "<br>" +
                "<strong>Tamanho:</strong> " + fileSizeMB + " MB<br>" +
                "<strong>Tipo:</strong> " + fileType;

            convertBtn.disabled = false;
        } else {
            videoPreview.style.display = "none";
            convertBtn.disabled = true;
        }
    });

    clearBtn.addEventListener("click", function() {
        videoInput.value = "";
        videoPreview.style.display = "none";
        convertBtn.disabled = true;
        loadingIndicator.style.display = "none";
        convertBtn.textContent = "Converter para MP4";
    });

    convertForm.addEventListener("submit", function(e) {
        if (!videoInput.files.length) {
            e.preventDefault();
            LevAI.toast("Por favor, selecione um vídeo!", "warning");
            return;
        }

        loadingIndicator.style.display = "block";
        convertBtn.disabled = true;
        convertBtn.textContent = "Convertendo...";
        videoPreview.style.display = "none";
    });
});
