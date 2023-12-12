// Description: JavaScript file for html templates containing comments in the quote app folder

/* Allows user to comment on a posted quote */

// DOM Content Event Listener
document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to all comment buttons
    const commentBtns = document.querySelectorAll('.comment-btn');
    commentBtns.forEach(commentBtn => {
        commentBtn.addEventListener('click', function(event) {
            event.preventDefault();
            // Get quoteId and hide comment button
            const quoteId = commentBtn.dataset.id;
            console.log(`Comment button event listener initiated. Quote id retrieved: ${quoteId}`);

            // Get comments div
            const postCommentView = document.querySelector(`#post-comment-${quoteId}`);

            let textArea, postBtn;

            // Create textarea and post button
            if (!postCommentView.querySelector('textarea') && !postCommentView.querySelector('button')) {
                textArea = document.createElement('textarea');
                textArea.classList.add('form-control');
                textArea.classList.add('mb-2');
                textArea.classList.add('card-text');
                textArea.name = 'content';
                textArea.placeholder = 'Comment';
                textArea.autofocus = true;
                textArea.style.width = '90%';

                postBtn = document.createElement('button');
                postBtn.classList.add('btn');
                postBtn.classList.add('btn-sm');
                postBtn.classList.add('mb-2');
                postBtn.textContent = 'Post';
                postBtn.style.fontSize = '0.8rem';

                // Append textarea and post button to comment view
                postCommentView.appendChild(textArea);
                postCommentView.appendChild(postBtn);
            } else {
                textArea = postCommentView.querySelector('textarea');
                postBtn = postCommentView.querySelector('button');
            }

            // Show comments view
            const commentsView = document.querySelector(`#comments-view-${quoteId}`);
            commentsView.style.display = 'block';

            // Add a click event listener to the post button
            postBtn.addEventListener('click', function() {
                const newCommentContent = textArea.value;
                fetch(`/comment/${quoteId}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        'content': newCommentContent,
                        'id': quoteId
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    textArea.remove();
                    postBtn.remove();
            
                    // Increase the comment count
                    const commentCount = document.getElementById(`comment-count-${quoteId}`);
                    commentCount.textContent = parseInt(commentCount.textContent) + 1;
            
                    // Create a new comment div
                    const newComment = document.createElement('div');
                    newComment.classList.add('comment-text');
                    newComment.textContent = newCommentContent;
            
                    // Append the new comment to the comments view
                    commentsView.appendChild(newComment);
            
                    // Display user information
                    const userInfo = document.createElement('div');
                    userInfo.textContent = `Posted by ${data.user.username} ${data.timestamp} ago`;
                    newComment.appendChild(userInfo);
                })
                .catch((error) => {
                    console.error('Error:', error);
                })
            });
        });
    }); 
});