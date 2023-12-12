// Description: JavaScript file for quote/profile.html

/* Controls profile page views. */

// JavaScript file for profile.html

document.addEventListener('DOMContentLoaded', function() {
    // Get all the view buttons
    const viewButtons = document.querySelectorAll('.view-button');

    // Add event listeners to all view buttons
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Hide all views
            document.querySelectorAll('.view').forEach(view => {
                view.style.display = 'none';
            });

            // Show the clicked view
            const viewId = this.dataset.view;
            document.getElementById(viewId).style.display = 'block';
        });
    });

    // Show the 'overview-view' by default
    document.getElementById('overview-view').style.display = 'block';
});
