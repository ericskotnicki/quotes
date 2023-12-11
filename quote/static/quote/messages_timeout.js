// Path: quote/templates/quote/layout.html

// This code loads all messages and then fades them out after 5 seconds.


// window.onload function is used to ensure that the DOM is loaded before the timeout function is called
window.onload = function () {
    setTimeout(function () {

        // Get all the alert elements
        let alerts = document.querySelectorAll('.alert');

        // Loop over the alert elements and hide them
        alerts.forEach(alert => alert.style.display = 'none');
    }, 5000);   // Alerts are hidden after 5 seconds

    // Log to the console that the flash messages timeout has been set
    console.log('Flash messages timeout set');
};
