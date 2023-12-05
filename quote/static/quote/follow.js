// Description: JavaScript file for quote/profile.html

/* Allows user to Follow/Unfollow other users */


// DOM Content Event Listener
document.addEventListener('DOMContentLoaded', function () {
    const followButton = document.querySelector('#follow-button');
    const unfollowButton = document.querySelector('#unfollow-button');

    if (followButton) {
        followButton.addEventListener('click', () => followUser());
    }

    if (unfollowButton) {
        unfollowButton.addEventListener('click', () => unfollowUser());
    }
});


// Follow User
function followUser() {
    const id = document.querySelector('#follow-button').dataset.id;
    fetch(`/follow/${id}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(result => {
        // Update follow button and follow count
        document.querySelector('#follow-button').style.display = 'none';
        document.querySelector('#unfollow-button').style.display = 'block';
        document.querySelector('#follow-count').innerHTML = parseInt(document.querySelector('#follow-count').innerHTML) + 1;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


// Unfollow User
function unfollowUser() {
    const id = document.querySelector('#unfollow-button').dataset.id;
    fetch(`/unfollow/${id}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(result => {
        // Update follow button and follow count
        document.querySelector('#unfollow-button').style.display = 'none';
        document.querySelector('#follow-button').style.display = 'block';
        document.querySelector('#follow-count').innerHTML = parseInt(document.querySelector('#follow-count').innerHTML) - 1;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}