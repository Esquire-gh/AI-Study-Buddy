function toggleAccordion(event, panelId) {
    event.preventDefault();
    var panel = document.getElementById(panelId);
    if (panel.style.display === "block") {
        panel.style.display = "none";
    } else {
        panel.style.display = "block";
    }
}


// load courses and files from canvas
$(document).ready(function() {
    // LOAD COURSES AND FILES FROM CANVAS AND DISPLAY IN MODAL
    $('#load-pdf-button').click(function() {
        $.ajax({
        url: '/load-course-files',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            window.location.reload()
        },
        error: function(error) {
            console.error("Error fetching data: ", error);
        }
        });
    });


    $("#update-convo-context").click(function() {
        var path = window.location.pathname;
        // Split the path into segments
        var segments = path.split('/');
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

       $.ajax({
            url: endpoint(selectedFiles.join(), chat_id),
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                window.alert(data.response)
            },
            error: function() {
                console.log("Error updating Context")
            }
       })
    });
});



document.getElementById('load-pdf-button').addEventListener('click', function() {
    // Add the wait cursor class to the body
    document.body.classList.add('wait');

    // Simulate a background operation with setTimeout
    setTimeout(function() {
        // Remove the wait cursor class after 3 seconds
        document.body.classList.remove('wait');
    }, 3000);
});

document.getElementById("update-convo-context").addEventListener('click', function() {
    // Add the wait cursor class to the body
    document.body.classList.add('wait');

    // Simulate a background operation with setTimeout
    setTimeout(function() {
        // Remove the wait cursor class after 3 seconds
        document.body.classList.remove('wait');
    }, 3000);
});


