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
                textArea.style.width = '100%';

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
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data);
                    // Remove the textarea and postBtn
                    textArea.remove();
                    postBtn.remove();
                
                    // Increase the comment count
                    const commentCount = document.getElementById(`comment-count-${quoteId}`);
                    commentCount.textContent = parseInt(commentCount.textContent) + 1;
                
                    // Access the user's info and comment timestamp
                    const username = data.user.username;
                    const profilePicture = data.user.profile_picture;
                    const commentText = data.comment.text;
                    const commentTimestamp = data.comment.timestamp;
                
                    // Create a new comment div
                    const newCommentDiv = document.createElement('div');
                    newCommentDiv.classList.add('mb-3'); // Add bottom margin
                
                    // Create a div for the user info and profile picture
                    const userInfoDiv = document.createElement('div');
                    userInfoDiv.classList.add('d-flex', 'align-items-center');
                    newCommentDiv.appendChild(userInfoDiv);
                
                    // Create and append the profile picture
                    const profilePic = document.createElement('img');
                    profilePic.classList.add('rounded-circle');
                    profilePic.src = profilePicture ? profilePicture : '#';
                    profilePic.alt = `${username}'s profile picture`;
                    profilePic.style.width = '40px';
                    profilePic.style.height = '40px';
                    userInfoDiv.appendChild(profilePic);
                
                    // Create and append the username and timestamp
                    const usernameP = document.createElement('p');
                    usernameP.classList.add('text-muted', 'small', 'mr-2');
                    usernameP.innerHTML = `Posted by <a href="/profile/${username}">/${username}</a>`;
                    const timestampP = document.createElement('p');
                    timestampP.classList.add('text-muted', 'small');
                    timestampP.textContent = commentTimestamp;
                    userInfoDiv.appendChild(usernameP);
                    userInfoDiv.appendChild(timestampP);
                
                    // Create and append the comment text
                    const commentP = document.createElement('p');
                    commentP.classList.add('comment-text');
                    commentP.textContent = commentText;
                    newCommentDiv.appendChild(commentP);
                
                    // Append the new comment to the comments view
                    const commentsView = document.getElementById(`comments-view-${quoteId}`);
                    commentsView.insertBefore(newCommentDiv, commentsView.firstChild);
                })
                .catch((error) => {
                    console.error('There was a problem with the fetch operation.', error);
                });
            });
        });
    }); 
});