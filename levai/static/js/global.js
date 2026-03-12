/* ========================================
   LevAI Global JavaScript
   ======================================== */

/* Global namespace */
window.LevAI = window.LevAI || {};

document.addEventListener("DOMContentLoaded", function() {

    /* ========== Lucide Icons ========== */
    if (typeof lucide !== "undefined") {
        lucide.createIcons();
    }

    /* ========== Theme toggle ========== */
    var themeToggle = document.getElementById("themeToggle");

    if (themeToggle) {
        themeToggle.addEventListener("click", function() {
            var current = document.documentElement.getAttribute("data-theme");
            var next = current === "dark" ? "light" : "dark";
            document.documentElement.setAttribute("data-theme", next);
            localStorage.setItem("theme", next);
        });
    }

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

    /* Close sidebar on link click (mobile) */
    if (sideBar) {
        var links = sideBar.querySelectorAll("a");
        for (var i = 0; i < links.length; i++) {
            links[i].addEventListener("click", function() {
                document.body.classList.remove("sidebar-open");
            });
        }
    }

    /* Close sidebar on Escape key (mobile) */
    document.addEventListener("keydown", function(e) {
        if (e.key === "Escape" && document.body.classList.contains("sidebar-open")) {
            document.body.classList.remove("sidebar-open");
        }
    });

    /* ========== Active sidebar link ========== */
    if (sideBar) {
        var currentPath = window.location.pathname;
        var sidebarLinks = sideBar.querySelectorAll("a[href]");

        for (var j = 0; j < sidebarLinks.length; j++) {
            var link = sidebarLinks[j];
            var href = link.getAttribute("href");

            if (href === "/") {
                if (currentPath === "/") {
                    link.classList.add("active");
                }
            } else if (currentPath.indexOf(href) === 0) {
                link.classList.add("active");
            }
        }
    }

    /* ========== Password toggle with Lucide ========== */
    var passwordInput = document.getElementById("password");
    var togglePassword = document.getElementById("togglePassword");
    var eyeIcon = document.getElementById("eyeIcon");

    if (passwordInput && togglePassword && eyeIcon) {
        togglePassword.addEventListener("click", function() {
            var isPassword = passwordInput.type === "password";
            passwordInput.type = isPassword ? "text" : "password";

            eyeIcon.setAttribute("data-lucide", isPassword ? "eye" : "eye-off");

            if (typeof lucide !== "undefined") {
                lucide.createIcons();
            }
        });
    }
});

/* ========== Toast Notification System ========== */

/**
 * Show a toast notification.
 * @param {string} message - The message to display.
 * @param {string} type - One of "success", "error", "warning", "info".
 * @param {number} duration - Auto-dismiss time in ms (default 4000).
 */
LevAI.toast = function(message, type, duration) {
    type = type || "info";
    duration = duration || 4000;

    var container = document.getElementById("toastContainer");
    if (!container) return;

    var iconMap = {
        "success": "check-circle",
        "error": "alert-circle",
        "warning": "alert-triangle",
        "info": "info"
    };

    var toast = document.createElement("div");
    toast.className = "toast toast-" + type;
    toast.innerHTML =
        "<i data-lucide=\"" + iconMap[type] + "\"></i>" +
        "<span class=\"toast-message\">" + message + "</span>" +
        "<button class=\"toast-close\" aria-label=\"Fechar\">&times;</button>";

    container.appendChild(toast);

    if (typeof lucide !== "undefined") {
        lucide.createIcons();
    }

    /* Close button */
    var closeBtn = toast.querySelector(".toast-close");
    closeBtn.addEventListener("click", function() {
        dismissToast(toast);
    });

    /* Auto-dismiss */
    var timer = setTimeout(function() {
        dismissToast(toast);
    }, duration);

    function dismissToast(el) {
        clearTimeout(timer);
        el.style.animation = "toastSlideOut 0.3s ease forwards";
        setTimeout(function() {
            if (el.parentNode) {
                el.parentNode.removeChild(el);
            }
        }, 300);
    }
};

/**
 * Show a custom confirm dialog (replaces native confirm()).
 * @param {string} message - The confirmation message.
 * @param {function} onConfirm - Callback if user confirms.
 */
LevAI.confirm = function(message, onConfirm) {
    /* Remove any existing confirm overlay */
    var existing = document.querySelector(".confirm-overlay");
    if (existing) {
        existing.parentNode.removeChild(existing);
    }

    var overlay = document.createElement("div");
    overlay.className = "confirm-overlay";
    overlay.innerHTML =
        "<div class=\"confirm-dialog\">" +
            "<p>" + message + "</p>" +
            "<div class=\"confirm-actions\">" +
                "<button class=\"btn btn-secondary confirm-cancel\">Cancelar</button>" +
                "<button class=\"btn btn-danger confirm-ok\">Confirmar</button>" +
            "</div>" +
        "</div>";

    document.body.appendChild(overlay);

    var cancelBtn = overlay.querySelector(".confirm-cancel");
    var okBtn = overlay.querySelector(".confirm-ok");

    function close() {
        if (overlay.parentNode) {
            overlay.parentNode.removeChild(overlay);
        }
    }

    cancelBtn.addEventListener("click", close);

    okBtn.addEventListener("click", function() {
        close();
        if (typeof onConfirm === "function") {
            onConfirm();
        }
    });

    /* Close on overlay background click */
    overlay.addEventListener("click", function(e) {
        if (e.target === overlay) {
            close();
        }
    });

    /* Close on Escape */
    var escHandler = function(e) {
        if (e.key === "Escape") {
            close();
            document.removeEventListener("keydown", escHandler);
        }
    };
    document.addEventListener("keydown", escHandler);
};
