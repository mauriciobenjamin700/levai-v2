document.addEventListener("DOMContentLoaded", function() {
    var form = document.getElementById("docForm");
    var fileInput = form ? form.querySelector("input[type='file']") : null;
    var fileInfo = document.getElementById("fileInfo");
    var fileName = document.getElementById("fileName");
    var fileSize = document.getElementById("fileSize");
    var convertBtn = document.getElementById("convertBtn");
    var clearBtn = document.getElementById("clearBtn");
    var loadingIndicator = document.getElementById("loadingIndicator");

    /* Mostrar info do arquivo selecionado */
    if (fileInput) {
        fileInput.addEventListener("change", function() {
            if (this.files.length > 0) {
                var file = this.files[0];
                var size = file.size;
                var sizeText = size < 1024
                    ? size + " B"
                    : size < 1048576
                        ? (size / 1024).toFixed(1) + " KB"
                        : (size / 1048576).toFixed(1) + " MB";

                fileName.textContent = file.name;
                fileSize.textContent = "(" + sizeText + ")";
                fileInfo.style.display = "flex";
            } else {
                fileInfo.style.display = "none";
            }
        });
    }

    /* Loading state ao submeter */
    if (form) {
        form.addEventListener("submit", function() {
            if (convertBtn) {
                convertBtn.disabled = true;
                convertBtn.textContent = "Convertendo...";
            }
            if (loadingIndicator) {
                loadingIndicator.style.display = "block";
            }
        });
    }

    /* Botao limpar */
    if (clearBtn) {
        clearBtn.addEventListener("click", function() {
            if (form) {
                form.reset();
            }
            if (fileInfo) {
                fileInfo.style.display = "none";
            }
            if (convertBtn) {
                convertBtn.disabled = false;
                convertBtn.textContent = "Converter para PDF";
            }
            if (loadingIndicator) {
                loadingIndicator.style.display = "none";
            }
        });
    }
});
