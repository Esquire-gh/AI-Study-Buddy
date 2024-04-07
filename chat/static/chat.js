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
        // var path = window.location.pathname;
        // // Split the path into segments
        // var segments = path.split('/');
        // // Get the chat_id
        // var chat_id = segments.pop();

        var chat_id = 1
        var user_input = encodeURIComponent(userInput)

        endpoint = (chat_id, user_input) => `get_chatbot_response/?chat_id=${chat_id}&input_message=${user_input}`

        fetch(endpoint(chat_id, user_input))
        .then(response => response.json())
        .then(data => {
                // Display the bot's response returned by the Django view
        displayBotMessage(data.response);
        })
        .catch(error => {console.log("Error sending message")});
        

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



