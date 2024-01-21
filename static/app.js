const socket = new WebSocket("ws://127.0.0.1:8000/ws/1");

var chatBody=document.getElementById("response");

socket.onopen = (event) => {
    console.log("WebSocket connection opened:", event);
};

socket.onmessage = (event) => {
    document.getElementById("message").value = ""; // Clear the input field
    const response = event.data;
    chatBody.innerHTML += '<div class="message bot-message">' + response + '</div>';
    chatBody.scrollTop = chatBody.scrollHeight;
};

socket.onclose = (event) => {
    console.log("WebSocket connection closed:", event);
};

function sendMessage() {
    var message = document.getElementById("message").value;
    var userMessage = '<div class="message user-message">' + message + '</div>';
    chatBody.innerHTML += userMessage;
    socket.send(message);
}
