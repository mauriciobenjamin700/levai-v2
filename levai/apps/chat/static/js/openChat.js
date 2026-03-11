function openChat(chatId) {
    var chatElement = document.getElementById("chat-" + chatId);
    if (chatElement) {
        window.location.href = "/chat/" + chatId + "/";
    }
}
