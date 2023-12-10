// Description: JavaScript file for html templates containing the edit button in the quote app folder

/* Allows a user to edit their posts */

// DOM Content Event Listener
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM Content Loaded (edit.js)")
    // Create variables to store edit link button, textarea, original quote content to fill textarea and save button
    let activeEditLink = null;
    let activeQuoteContent = null;
    let activeTextArea = null;
    let activeSaveBtn = null;

    // Get all edit links and add a click event listener to each
    const editLinks = document.querySelectorAll('.edit-link');
    editLinks.forEach(editLink => {

        // If edit link is clicked show
        editLink.addEventListener('click', function(event) {
            event.preventDefault();
            // Set activeEditLink to current editLink
            activeEditLink = editLink;

            // If active edit link, show it
            if (activeEditLink) {
                activeEditLink.style.display = 'block';
            }
            // If there is an active textarea/save button, remove them
            if (activeTextArea && activeSaveBtn) {
                activeTextArea.remove();
                activeSaveBtn.remove();

                if (activeQuoteContent) {
                    activeQuoteContent.style.display = 'block';
                }
            }
            
            // Get the quote id from the edit link then hide the link
            const quoteId = editLink.dataset.id;
            editLink.style.display = 'none';
            console.log(`Edit link event listener initiated. Post id retrieved: ${quoteId}`);

            // Get quote content from quote content element and add it to activeQuoteContent variable
            const quoteContent = document.querySelector(`#quote-content-${quoteId}`);
            quoteContent.style.display = 'none';
            activeQuoteContent = quoteContent
            console.log(`Retrieved quote content: ${quoteContent.textContent}`)

            // Create div container for textarea and save button
            const textarea = document.createElement('textarea')
            textarea.classList.add('form-control');
            textarea.classList.add('mb-2');
            textarea.name = 'content';
            textarea.autofocus = true;
            // Display original quote content in textarea
            textarea.value = quoteContent.textContent;

            const saveBtn = document.createElement('button');
            saveBtn.classList.add('btn');
            saveBtn.textContent = 'Save';

            // Set the active textarea and save button
            activeTextArea = textarea;
            activeSaveBtn = saveBtn;

            console.log('Created textarea & save button. Waiting for save button event listener click');


            // Add a click event listener to the save button
            saveBtn.addEventListener('click', function() {
                // Update the quote content and show it
                quoteContent.textContent = textarea.value;
                quoteContent.style.display = 'block';
                // Log new quote content to the console
                console.log(`Retrieved edit quote content: ${quoteContent.textContent}`);

                // Remove the textarea & save button
                textarea.remove();
                saveBtn.remove();

                // Clear the active textarea, save button and quote content
                activeTextArea = null;
                activeSaveBtn = null;
                activeQuoteContent = null;

                // Show active edit link
                activeEditLink.style.display = 'block';
                activeEditLink = null;

                // Show the edit link
                editLink.style.display = 'block';

                // Get the CSRF token
                // const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];

                // Send edited quote content to server (edit view) via PUT request
                fetch(`/edit/${quoteId}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        'content': quoteContent.textContent
                        // Include the CSRF token in the 'X-CSRFToken' header
                        // 'X-CSRFToken': csrftoken
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                })
            });

            // Insert the textarea and save button after the quote content
            quoteContent.parentNode.insertBefore(textarea, quoteContent.nextSibling);
            quoteContent.parentNode.insertBefore(saveBtn, textarea.nextSibling);
        });
    });
});
