function toggleAccordion(event, panelId) {
    event.preventDefault();
    var panel = document.getElementById(panelId);
    if (panel.style.display === "block") {
        panel.style.display = "none";
    } else {
        panel.style.display = "block";
    }
}

// Close the modal
document.getElementsByClassName('close-button')[0].onclick = function() {
    document.getElementById('pdf-modal').style.display = 'none';
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


// load courses and files from canvas
$(document).ready(function() {
    $('#load-pdf-button').click(function() {
        $.ajax({
        url: '/load-course-files',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var content = '';

            var accordionSubItem = (fileId, fileName) => `
                <label>
                    <p>
                        <input type="checkbox" name="${fileId}" />
                        <span>${fileName}</span>
                    </p>
                </label>
            `
            var accordionItem = (courseId, courseName, accordionSubItems) => `
            <div class="accordion-item">
                <button class="accordion-button" onclick="toggleAccordion(event, '${courseId}')">${courseName}</button>
                <div class="panel" id="${courseId}">
                ${accordionSubItems}
                </div>
            </div>
            `
            // Iterate over each item in the array
            $.each(data.course_files, function(index, course) {
                // Construct HTML for each 
                
                var fileTemplates = ''
                $.each(course.files, function(index, file) {
                    // Construct HTML for each 
                    fileTemplates += accordionSubItem(file.id, file.name)
                });

                content += accordionItem(course.id, course.name, fileTemplates)
            });

            // Update the modal's content and show it
            $('#canvas-courses-accordion').html(content);
            $('#pdf-modal').modal('show');
        },
        error: function(error) {
            console.error("Error fetching data: ", error);
        }
        });
    });
});