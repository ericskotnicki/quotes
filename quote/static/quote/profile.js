// Description: JavaScript file for quote/profile.html

/* Controls profile page views. */

// DOM Content Event listener
document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#overview-view').addEventListener('click', () => loadProfile('overview'));
    document.querySelector('#posts-view').addEventListener('click', () => loadProfile('posts'));
    document.querySelector('#comments-view').addEventListener('click', () => loadProfile('comments'));
    document.querySelector('#saved-view').addEventListener('click', () => loadProfile('saved'));
    document.querySelector('#liked-view').addEventListener('click', () => loadProfile('liked'));
    document.querySelector('#history-view').addEventListener('click', () => loadProfile('history'));

    // By default, load 'posts' view
    loadProfile('posts');
});


// Load Profile Views
function loadProfile(view) {

    // Show the posts view
    document.querySelector('#overview-view').style.display = 'none';
    document.querySelector('#posts-view').style.display = 'block';
    document.querySelector('#comments-view').style.display = 'none';
    document.querySelector('#saved-view').style.display = 'none';
    document.querySelector('#liked-view').style.display = 'none';
    document.querySelector('#history-view').style.display = 'none';

    // Show the view name
    document.querySelector('#profile-view').innerHTML = `<h2>${view.charAt(0).toUpperCase() + view.slice(1)}</h2>`;

    // Access user profile info
    // fetch(`/profile/${}`)
}