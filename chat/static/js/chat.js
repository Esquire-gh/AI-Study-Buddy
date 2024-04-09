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

    function getChatbotResponse(userInput) {
        var path = window.location.pathname;
        // Split the path into segments
        var segments = path.split('/');
        segments.pop()
        // Get the chat_id
        var chat_id = segments.pop();

        if (chat_id == "chat") {
            chat_id = ""
        }

        var user_input = encodeURIComponent(userInput)

        endpoint = (id, input) => `/get_chatbot_response/?chat_id=${id}&input_message=${input}`

        fetch( window.location.origin +  endpoint(chat_id, user_input))
        .then(response => response.json())
        .then(data => {
            // Display the bot's response returned by the Django view
            displayBotMessage(data.response);

            if (data.redirect) {
                window.location.replace(data.redirect)
            }
        })
        .catch(error => {console.log("Error sending message")});
    }

    function displayBotMessage(message) {
        const botMessageDiv = document.createElement('div');
        botMessageDiv.classList.add('message', 'bot-message');
        botMessageDiv.textContent = message;
        chatWindow.appendChild(botMessageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to the latest message
    }
});



