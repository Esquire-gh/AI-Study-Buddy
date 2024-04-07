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
            // var content = '';

            // var accordionSubItem = (fileId, fileName, inputVal) => `
            //     <label>
            //         <p>
            //             <input type="checkbox" name="${fileId}" class="canvas_course_file" value="${inputVal}" />
            //             <span>${fileName}</span>
            //         </p>
            //     </label>
            // `
            // var accordionItem = (courseId, courseName, accordionSubItems) => `
            // <div class="accordion-item">
            //     <button class="accordion-button" onclick="toggleAccordion(event, '${courseId}')">${courseName}</button>
            //     <div class="panel" id="${courseId}">
            //     ${accordionSubItems}
            //     </div>
            // </div>
            // `
            // // Iterate over each item in the array
            // $.each(data.course_files, function(index, course) {
            //     // Construct HTML for each 
                
            //     var fileTemplates = ''
            //     $.each(course.files, function(index, file) {
            //         var val = {
            //             "course_name": course.name,
            //             "course_external_id": course.id,
            //             "file_name": file.name,
            //             "file_external_id": file.id,
            //             "file_url": file.url
            //         }
            //         fileTemplates += accordionSubItem(file.id, file.name, JSON.stringify(val))
            //     });

            //     content += accordionItem(course.id, course.name, fileTemplates)
            // });

            // // Update the modal's content and show it
            // $('#canvas-courses-accordion').html(content);
            // $('#pdf-modal').modal('show');
        },
        error: function(error) {
            console.error("Error fetching data: ", error);
        }
        });
    });


    // // SEND ALL SELECTED FILES TO BACKEND FOR TOKENIZATOIN
    // $('#send-button').click(function() {
    //     var userInput = $('#user-input').val()

    //     var endpoint = (input) => `send_message?message=${input}`
    //     $.ajax({
    //         url: endpoint(userInput),
    //         type: 'GET',
    //         dataType: 'json',
    //         success: function(data) {
                
    //             window.alert(data.response)
    //         },
    //         error: function(error) {
    //             console.error("Error sending selected files: ", error);
    //         }
    //     });
    // });
});

document.getElementById('load-pdf-button').addEventListener('click', function() {
    // Show the beachball
    document.getElementById('beachball-container').classList.remove('hidden');
    document.getElementById("load-pdf-button").disabled = true
    document.getElementById("send-button").disabled = true
    document.getElementById("update-convo-context").disabled = true
   

    // Simulate loading process (e.g., fetching data)
    setTimeout(() => {
        // Hide the beachball after 3 seconds
        document.getElementById('beachball-container').classList.add('hidden');
        document.getElementById("load-pdf-button").disabled = false
        document.getElementById("send-button").disabled = false
        document.getElementById("update-convo-context").disabled = false
        
    }, 3000);
});



