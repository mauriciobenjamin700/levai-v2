console.log("openChat.js loaded");
async function openChat(chatId) {
    const chatElement = document.getElementById(`chat-${chatId}`);
    console.log(`Opening chat with ID: ${chatId}`);
    console.log(chatElement);
    if (chatElement) {
        window.location.href = `/chat/${chatId}/`;
    } else {
        console.error(`Chat with ID ${chatId} not found.`);
    }
}