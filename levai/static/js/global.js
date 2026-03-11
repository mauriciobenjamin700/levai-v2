document.addEventListener("DOMContentLoaded", function() {
    /* ========== Sidebar toggle (mobile) ========== */
    var menuToggle = document.getElementById("menuToggle");
    var overlay = document.getElementById("sidebarOverlay");
    var sideBar = document.getElementById("sideBar");

    if (menuToggle) {
        menuToggle.addEventListener("click", function() {
            document.body.classList.toggle("sidebar-open");
        });
    }

    if (overlay) {
        overlay.addEventListener("click", function() {
            document.body.classList.remove("sidebar-open");
        });
    }

    /* Fechar sidebar ao clicar em link (mobile) */
    if (sideBar) {
        var links = sideBar.querySelectorAll("a");
        for (var i = 0; i < links.length; i++) {
            links[i].addEventListener("click", function() {
                document.body.classList.remove("sidebar-open");
            });
        }
    }

    /* ========== Password toggle ========== */
    var passwordInput = document.getElementById("password");
    var togglePassword = document.getElementById("togglePassword");
    var eyeIcon = document.getElementById("eyeIcon");

    if (passwordInput && togglePassword && eyeIcon) {
        togglePassword.addEventListener("click", function() {
            var isPassword = passwordInput.type === "password";
            passwordInput.type = isPassword ? "text" : "password";
            eyeIcon.src = isPassword
                ? "/static/images/eyesopen.svg"
                : "/static/images/eyesclose.svg";
        });
    }
});
