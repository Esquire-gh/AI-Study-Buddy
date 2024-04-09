// GLOBAL FUNCTIONS - NECESSARY FOR SETTINGS EVENT FROM WITHIN HTML
function toggleAccordion(event, panelId) {
    event.preventDefault();
    var panel = document.getElementById(panelId);
    if (panel.style.display === "block") {
        panel.style.display = "none";
    } else {
        panel.style.display = "block";
    }
}

function toggleDisableKeyButtons(toggle) {
    buttons = document.querySelectorAll('.keyButton');

    buttons.forEach(button => {
        button.disabled = toggle
    });
}


// PURE JS
document.addEventListener('DOMContentLoaded', function() {
    // LOAD COURSES AND FILES FROM CANVAS AND DISPLAY IN MODAL
    $('#load-pdf-button').click(function() {
        toggleDisableKeyButtons(true);

        fetch("/load-course-files", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then((response) => {
            if (!response.ok) {
                return response.json().then((json) => {
                    throw new Error(json.error)
                })
            }
            return response.json()
        })
        .then((json) => {
            window.alert(json.response)
            toggleDisableKeyButtons(false);
        })
        .catch(error => {
            window.alert(error)
            toggleDisableKeyButtons(false)
        })
    });


    $("#update-convo-context").click(function() {
        var path = window.location.pathname;
        // Split the path into segments
        var segments = path.split('/');
        segments.pop()
        // Get the chat_id
        var chat_id = segments.pop();

        // get all files selected and get their ids
        var selectedFiles = $(".select_files:checked").map(function() {
            return this.value;
        }).get()

        if (chat_id == "chat" || chat_id == "") {
            chat_id = "new"
        }
        var endpoint = (input, chat_id) => `/tokenize-files?file_ids=${input}&chat_id=${chat_id}`;

        toggleDisableKeyButtons(true);

        fetch(
            endpoint(selectedFiles.join(), chat_id),
            {
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        )
        .then(response => {
            if (!response.ok) {
                return response.json().then(json => {
                    throw new Error(json.error)
                })
            }
            return response.json()
        })
        .then((json) => {
            toggleDisableKeyButtons(false);
            window.alert(json.response)
        })
        .catch((error) => {
            window.alert(error)
            toggleDisableKeyButtons(false);
        });
    });

    var chatHistory = document.getElementById("messageBody");
    chatHistory.scrollTop = chatHistory.scrollHeight;
});