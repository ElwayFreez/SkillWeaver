const input = document.getElementById("input");
const sendBtn = document.getElementById("send-btn");
const chat = document.getElementById("chat-window");

function addMessage(text, role) {
    const msg = document.createElement("div");
    msg.className = "message " + role;
    msg.textContent = text;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    // временное сообщение робота
    addMessage("...", "bot");

    const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: text })
    });

    const data = await response.json();

    // заменяем последнее сообщение бота на реальный ответ
    const botMessages = document.querySelectorAll(".message.bot");
    botMessages[botMessages.length - 1].textContent = data.response;
}

sendBtn.onclick = sendMessage;

input.onkeydown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
};
