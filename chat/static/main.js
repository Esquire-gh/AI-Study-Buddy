function toggleAccordion(event, panelId) {
    event.preventDefault();
    var panel = document.getElementById(panelId);
    if (panel.style.display === "block") {
        panel.style.display = "none";
    } else {
        panel.style.display = "block";
    }
}

// // Close the modal
// document.getElementsByClassName('close-button')[0].onclick = function() {
//     document.getElementById('pdf-modal').style.display = 'none';
// };

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
        // var path = window.location.pathname;
        // // Split the path into segments
        // var segments = path.split('/');
        // // Get the chat_id
        // var chat_id = segments.pop();

        // get all files selected and get their ids
        var selectedFiles = $(".select_files:checked").map(function() {
            return this.value;
        }).get()

        var convoId = "new";

        var chat_id = 1;

        var endpoint = (input, chat_id) => `tokenize-files?file_ids=${input}&chat_id=${chat_id}`;

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
