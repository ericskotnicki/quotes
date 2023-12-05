


// Add event listener to like buttons
document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', function() {
        const id = this.dataset.id;
        fetch(`/like/${id}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(result => {
            // Update like count
            document.querySelector(`#like-count-${id}`).innerHTML = result.like_count;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});