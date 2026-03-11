document.addEventListener("DOMContentLoaded", function() {
    var videoInput = document.getElementById("video");
    var videoPreview = document.getElementById("videoPreview");
    var previewVideo = document.getElementById("previewVideo");
    var videoInfo = document.getElementById("videoInfo");
    var convertBtn = document.getElementById("convertBtn");
    var clearBtn = document.getElementById("clearBtn");
    var loadingIndicator = document.getElementById("loadingIndicator");
    var videoForm = document.getElementById("videoForm");

    videoInput.addEventListener("change", function() {
        var file = this.files[0];

        if (file) {
            var url = URL.createObjectURL(file);
            previewVideo.src = url;
            videoPreview.style.display = "block";

            var fileSizeMB = (file.size / 1024 / 1024).toFixed(2);
            videoInfo.textContent = file.name + " - " + fileSizeMB + " MB";

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
    });

    videoForm.addEventListener("submit", function(e) {
        if (!videoInput.files.length) {
            e.preventDefault();
            alert("Por favor, selecione um video!");
            return;
        }

        loadingIndicator.style.display = "block";
        convertBtn.disabled = true;
        convertBtn.textContent = "Convertendo...";
    });
});
