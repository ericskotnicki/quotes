// Description: JavaScript file for html templates containing the Bookmark button/icon in the quote app folder

/* Allows user to bookmark a posted quote */

// DOM Content Event Listener
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.bookmark-btn').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const quoteId = button.dataset.id;
            fetch(`/bookmark/${quoteId}`, {
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
                return response.json();
            })
            .then(data => {
                console.log(data);   // bookmarked_by, user_bookmarked

                const icon = document.querySelector(`#bookmark-icon-${quoteId}`);
        
                if (data.user_bookmarked) {
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                } else {
                    icon.classList.remove('fas');
                    icon.classList.add('far');
                }
        
                // Update the bookmarked attribute of the icon
                icon.dataset.userBookmarked = data.user_bookmarked;
        
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        });
    });
});