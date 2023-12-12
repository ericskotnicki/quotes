// Path: quote/static/quote/main.js

/*

--> Ideas for JavaScript Enhancements

1. Dynamic Loading of Quotes: Instead of loading all quotes at once, use JavaScript to load them dynamically as the user scrolls down the page. This is often called "infinite scrolling" and can improve performance and user experience.
2. Form Validation: Use JavaScript to validate form inputs on the client side before they're submitted to the server. This can provide immediate feedback to the user and reduce server load.
3. Interactive Search: JavaScript can be used to implement a search feature that displays results as the user types, improving usability.
4. (DONE) Quote Rating or Liking System: If you plan to implement a system for users to rate or like quotes, JavaScript can be used to submit these ratings or likes without requiring a page reload.
5. User Profile Interactions: JavaScript can be used to enhance interactions on user profile pages. For example, you could use JavaScript to allow users to follow or unfollow other users without a page reload.
6. Animations and Transitions: JavaScript can be used to add animations and transitions to improve the visual appeal of your website.
7. (DONE) AJAX: AJAX stands for Asynchronous JavaScript and XML. It's a technique that allows web pages to be updated asynchronously by exchanging data with a web server behind the scenes. This means that it's possible to update parts of a web page, without reloading the whole page.
8. (DONE) Editing Quotes: You could use JavaScript to allow users to edit quotes without a page reload. This would involve using AJAX to submit the edited quote to the server and then updating the quote on the page with the new text.
*/


/* 

--> Infinite Scrolling - Dynamic Loading of Quotes

1. Detect when the user has scrolled to the bottom of the page and load more quotes dynamically using jQuery and AJAX.
2. load_more_quotes() function in views.py takes a parameter indicating how many quotes have already been loaded. It returns a JSON response containing the next 20 quotes.
3. The JSON response is parsed in main.js and the quotes are added to the page.
*/

$(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() == $(document).height()) {
        var start = $('#quotes').children().length;
        $.get('/load_more_quotes/', {start: start}, function(data) {
            var quotes = JSON.parse(data);
            for (var i = 0; i < quotes.length; i++) {
                var quote = quotes[i].fields;
                // Append the new quote to the #quotes element
                $('#quotes').append('<p>' + quote.quote + '</p>');
            }
        });
    }
});