// Description: JavaScript file for html templates containing the like (heart) button in the quote app folder

/* Allows user to like a posted quote from another user */

// DOM Content Event Listener
document.addEventListener('DOMContentLoaded', function () {

    // If user clicks on the like button, send a POST request to /like view
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            // Get quote id from button element
            const quoteId = button.dataset.id;
            
            // Send POST request to /like server-side view
            fetch(`/like/${quoteId}`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin',
                body: JSON.stringify({
                    'quote_id': quoteId
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();    // Retrieve response from /like server-side view
            })
            // Data contains likes, liked_by, and user_liked
            .then(data => {
                console.log(data);

                // Get the icon using its id
                const icon = document.querySelector(`#like-icon-${quoteId}`);
        
                // Check if the user has liked the quote
                if (data.user_liked) {
                    // If the user has liked the quote, add the 'fas' class and remove the 'far' class
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                } else {
                    // If the user has not liked the quote, add the 'far' class and remove the 'fas' class
                    icon.classList.remove('fas');
                    icon.classList.add('far');
                }
        
                // Update the data-user-liked attribute of the icon
                icon.dataset.userLiked = data.user_liked;
        
                // Update the like count for this quote
                document.querySelector(`#like-count-${quoteId}`).textContent = data.likes;
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        });
    });
});