$(document).ready(function() {
    // Check if dark mode was previously enabled
    if (localStorage.getItem('dark-mode') === 'true') {
        $('body').addClass('dark-theme');
    } else if (localStorage.getItem('dark-mode') === 'false') {
        $('body').removeClass('dark-theme');
    }

    // Add click event listener to the toggle button
    $('#theme-toggle').click(function() {
        $('body').toggleClass('dark-theme');

        // Save dark mode state
        if ($('body').hasClass('dark-theme')) {
            localStorage.setItem('dark-mode', 'true');
        } else {
            localStorage.setItem('dark-mode', 'false');
        }
    });
});