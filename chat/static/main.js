function toggleAccordion(event, panelId) {
    event.preventDefault();
    var panel = document.getElementById(panelId);
    if (panel.style.display === "block") {
        panel.style.display = "none";
    } else {
        panel.style.display = "block";
    }
}

document.getElementById('load-pdf-button').onclick = function() {
    document.getElementById('pdf-modal').style.display = 'block';
};

// Close the modal
document.getElementsByClassName('close-button')[0].onclick = function() {
    document.getElementById('pdf-modal').style.display = 'none';
};

// Load the selected PDF into the iframe
document.getElementById('pdf-file-input').onchange = function(event) {
    var selectedFile = event.target.files[0];
    var reader = new FileReader();

    reader.onload = function(e) {
        var pdfDisplay = document.getElementById('pdf-display');
        pdfDisplay.style.display = 'block';
        pdfDisplay.src = e.target.result;
        document.getElementById('pdf-modal').style.display = 'none';
    };

    reader.readAsDataURL(selectedFile);
};

document.getElementById('send-button').onclick = function() {
    var userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== '') {
        // Process the user input (e.g., append to chat window, send to server)
        console.log(userInput); // Placeholder for actual functionality

        // Clear the input field after sending the message
        document.getElementById('user-input').value = '';
    }
};