/**
 * Task calendar JavaScript module.
 * Handles modal interactions for creating, editing, and deleting tasks.
 */
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("taskModal");
    var form = document.getElementById("taskForm");
    var modalTitle = document.getElementById("modalTitle");
    var deleteBtn = document.getElementById("deleteBtn");
    var taskIdField = document.getElementById("taskId");
    var taskTitleField = document.getElementById("taskTitle");
    var taskDescriptionField = document.getElementById("taskDescription");
    var taskDateField = document.getElementById("taskDate");
    var taskTimeField = document.getElementById("taskTime");
    var taskPriorityField = document.getElementById("taskPriority");
    var taskStatusField = document.getElementById("taskStatus");

    /* Store previously focused element for accessibility */
    var previousFocus = null;

    /**
     * Get all focusable elements inside the modal for focus trap.
     */
    function getFocusableElements() {
        if (!modal) return [];
        return modal.querySelectorAll(
            "input, select, textarea, button, [tabindex]:not([tabindex=\"-1\"])"
        );
    }

    /**
     * Focus trap handler for Tab key inside modal.
     */
    function trapFocus(e) {
        if (e.key !== "Tab") return;

        var focusable = getFocusableElements();
        if (focusable.length === 0) return;

        var first = focusable[0];
        var last = focusable[focusable.length - 1];

        if (e.shiftKey) {
            if (document.activeElement === first) {
                e.preventDefault();
                last.focus();
            }
        } else {
            if (document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        }
    }

    /**
     * Open the modal with animation.
     */
    function showModal() {
        if (!modal) return;
        previousFocus = document.activeElement;
        modal.classList.add("active");
        modal.addEventListener("keydown", trapFocus);

        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }
    }

    /**
     * Open the modal for creating a new task on a specific date.
     */
    window.openCreateModal = function(year, month, day) {
        if (!form || !modal) return;

        form.reset();
        taskIdField.value = "";
        form.action = "/task/create/";
        modalTitle.textContent = "Nova Tarefa";
        deleteBtn.style.display = "none";

        var dateStr = year + "-" + String(month).padStart(2, "0") + "-" + String(day).padStart(2, "0");
        taskDateField.value = dateStr;
        taskPriorityField.value = "medium";
        taskStatusField.value = "pending";

        showModal();
        taskTitleField.focus();
    };

    /**
     * Open the modal for creating a task for today (FAB button).
     */
    window.openCreateModalToday = function() {
        var today = new Date();
        window.openCreateModal(today.getFullYear(), today.getMonth() + 1, today.getDate());
    };

    /**
     * Open the modal for editing an existing task.
     * Fetches task data via AJAX.
     */
    window.openEditModal = function(taskId, event) {
        if (event) {
            event.stopPropagation();
        }
        if (!form || !modal) return;

        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/task/" + taskId + "/");
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhr.onload = function() {
            if (xhr.status === 200) {
                var task = JSON.parse(xhr.responseText);

                taskIdField.value = task.id;
                taskTitleField.value = task.title;
                taskDescriptionField.value = task.description || "";
                taskDateField.value = task.date;
                taskTimeField.value = task.time || "";
                taskPriorityField.value = task.priority;
                taskStatusField.value = task.status;

                form.action = "/task/" + task.id + "/update/";
                modalTitle.textContent = "Editar Tarefa";
                deleteBtn.style.display = "inline-flex";

                showModal();
                taskTitleField.focus();
            }
        };
        xhr.onerror = function() {
            LevAI.toast("Erro ao buscar tarefa", "error");
        };
        xhr.send();
    };

    /**
     * Close the task modal with animation.
     */
    window.closeModal = function() {
        if (modal) {
            modal.classList.remove("active");
            modal.removeEventListener("keydown", trapFocus);

            if (previousFocus) {
                previousFocus.focus();
                previousFocus = null;
            }
        }
    };

    /**
     * Delete a task via dynamically created form.
     */
    window.deleteTask = function() {
        var taskId = taskIdField.value;
        if (!taskId) return;

        LevAI.confirm("Deseja excluir esta tarefa?", function() {
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
            if (!csrfToken) return;

            var deleteForm = document.createElement("form");
            deleteForm.method = "POST";
            deleteForm.action = "/task/" + taskId + "/delete/";

            var csrfInput = document.createElement("input");
            csrfInput.type = "hidden";
            csrfInput.name = "csrfmiddlewaretoken";
            csrfInput.value = csrfToken.value;
            deleteForm.appendChild(csrfInput);

            document.body.appendChild(deleteForm);
            deleteForm.submit();
        });
    };

    /* Close modal when clicking the overlay background */
    if (modal) {
        modal.addEventListener("click", function(e) {
            if (e.target === modal) {
                window.closeModal();
            }
        });
    }

    /* Close modal on Escape key */
    document.addEventListener("keydown", function(e) {
        if (e.key === "Escape" && modal && modal.classList.contains("active")) {
            window.closeModal();
        }
    });
});
