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

            // Send POST request to /follow or /unfollow
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













// // DOM Content Event Listener
// document.addEventListener('DOMContentLoaded', function () {
//     document.querySelectorAll('.follow-button').forEach(button => {
//         button.addEventListener('click', function () {
//             const userId = button.dataset.id;
//             const action = button.textContent.trim().toLowerCase();

//             fetch(`/${action}/${userId}`, {
//                 method: 'POST',
//                 body: JSON.stringify({
//                     user_id: userId
//                 }),
//                 headers: {
//                     'X-CSRFToken': getCookie('csrftoken'),
//                     'Accept': 'application/json',
//                     'Content-Type': 'application/json'
//                 }
//             })
//             .then(response => response.json())
//             .then(data => {
//                 button.textContent = data.user_followed ? 'Unfollow' : 'Follow';
//                 document.querySelector('#follow-count').textContent = data.followers;
//             });
//         });
//     });
// });

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }




// // DOM Content Event Listener
// document.addEventListener('DOMContentLoaded', function () {
//     const followButtons = document.querySelectorAll('.follow-button');
//     const unfollowButtons = document.querySelectorAll('.unfollow-button');

//     followButtons.forEach(button => {
//         button.addEventListener('click', () => followUser(button));
//     });

//     unfollowButtons.forEach(button => {
//         button.addEventListener('click', () => unfollowUser(button));
//     });
// });

// // Follow User
// function followUser(button) {
//     const id = button.dataset.id;
//     fetch(`/follow/${id}`, {
//         method: 'POST'
//     })
//     .then(response => response.json())
//     .then(result => {
//         // Update follow button and follow count
//         button.style.display = 'none';
//         button.nextElementSibling.style.display = 'block';
//         document.querySelector('#follow-count').innerHTML = parseInt(document.querySelector('#follow-count').innerHTML) + 1;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// }

// // Unfollow User
// function unfollowUser(button) {
//     const id = button.dataset.id;
//     fetch(`/unfollow/${id}`, {
//         method: 'POST'
//     })
//     .then(response => response.json())
//     .then(result => {
//         // Update follow button and follow count
//         button.style.display = 'none';
//         button.previousElementSibling.style.display = 'block';
//         document.querySelector('#follow-count').innerHTML = parseInt(document.querySelector('#follow-count').innerHTML) - 1;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// }