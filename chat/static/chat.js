document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-button');
    const userInputField = document.getElementById('user-input');
    const chatWindow = document.querySelector('.chat-window');

    sendButton.addEventListener('click', function() {
        const userText = userInputField.value;
        displayUserMessage(userText);
        getChatbotResponse(userText);
        userInputField.value = '';
    });

    userInputField.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });


    function displayUserMessage(message) {
        const userMessageDiv = document.createElement('div');
        userMessageDiv.classList.add('message', 'user-message');
        userMessageDiv.textContent = message;
        chatWindow.appendChild(userMessageDiv);
    }

    function getChatbotResponse() {
        fetch("get_chatbot_response/")
        .then(response => response.json())
        .then(data => {
                // Display the bot's response returned by the Django view
        displayBotMessage(data.bot_response);
        })
        .catch(error => console.error(error));
        

        // displayBotMessage(botResponse);
    }

    function displayBotMessage(message) {
        const botMessageDiv = document.createElement('div');
        botMessageDiv.classList.add('message', 'bot-message');
        botMessageDiv.textContent = message;
        chatWindow.appendChild(botMessageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to the latest message
    }

    


 
});



