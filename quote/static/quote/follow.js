// Description: JavaScript file for html templates containing the follow/unfollow button in the quote app folder

/* Allows user to Follow/Unfollow other users */

// DOM Content Event Listener
document.addEventListener('DOMContentLoaded', function () {
    // Add event listeners to all follow/unfollow buttons
    document.querySelectorAll('.follow-button, .unfollow-button').forEach(button => {
        button.addEventListener('click', function () {
            const userId = button.dataset.id;

            // Get the current button text and trim any leading/trailing whitespace
            const buttonText = button.textContent.trim();

            // Convert the button text to lowercase
            const buttonTextLowercase = buttonText.toLowerCase();

            // Determine the action based on the button text
            let action;
            if (buttonTextLowercase == 'follow') {
                action = 'follow';
            } else {
                action = 'unfollow';
            }

            // Send POST request to /follow or /unfollow view
            fetch(`/${action}/${userId}`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin',
                body: JSON.stringify({
                    'user_id': userId
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Update all follow/unfollow buttons and follow counts for this user
                document.querySelectorAll(`[data-id='${userId}']`).forEach(button => {
                    if (data.user_followed) {
                        button.textContent = 'Unfollow';
                        button.className = 'unfollow-button';
                    } else {
                        button.textContent = 'Follow';
                        button.className = 'follow-button';
                    }
                });
                // Update follow count for this user
                document.querySelectorAll('#follow-count-' + userId).forEach(followCount => {
                    followCount.textContent = 'Followers: ' + data.followers;
                });
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        });
    });
});
