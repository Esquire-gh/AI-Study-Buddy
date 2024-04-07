document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-button');
    const userInputField = document.getElementById('user-input');
    const chatWindow = document.querySelector('.chat-window');

    sendButton.addEventListener('click', function() {
        const userText = userInputField.value;
        displayUserMessage(userText);
        fetch(`/chat_response/?message=${encodeURIComponent(userText)}`)
            .then(response => response.json())
            .then(data => displayBotMessage(data.bot_response));
        userInputField.value = '';
    });