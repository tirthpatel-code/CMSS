// Complaint Detail JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const statusForm = document.getElementById('statusForm');
    const commentForm = document.getElementById('commentForm');
    const assignBtn = document.getElementById('assign-btn');
    const assignSelect = document.getElementById('assign-select');

    // Update status
    if (statusForm) {
        statusForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const status = document.getElementById('status-select').value;
            const resolutionNotes = document.getElementById('resolution-notes').value;

            try {
                const response = await fetch(`/api/complaint/${ticketNumber}/status/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({
                        status: status,
                        resolution_notes: resolutionNotes,
                    }),
                });

                const result = await response.json();

                if (result.success) {
                    location.reload();
                } else {
                    alert('Failed to update status: ' + (result.error || 'Unknown error'));
                }
            } catch (error) {
                alert('An error occurred. Please try again.');
            }
        });
    }

    // Add comment
    if (commentForm) {
        commentForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const commentText = document.getElementById('comment-text').value;
            const isInternal = document.getElementById('is-internal')?.checked || false;

            if (!commentText.trim()) {
                alert('Please enter a comment');
                return;
            }

            try {
                const response = await fetch(`/api/complaint/${ticketNumber}/comment/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({
                        comment: commentText,
                        is_internal: isInternal,
                    }),
                });

                const result = await response.json();

                if (result.success) {
                    // Add comment to the list
                    const commentsList = document.getElementById('comments-list');
                    const commentDiv = document.createElement('div');
                    commentDiv.className = `comment-item ${result.comment.is_internal ? 'comment-internal' : ''}`;
                    commentDiv.innerHTML = `
                        <div class="comment-header">
                            <strong>${result.comment.user}</strong>
                            ${result.comment.is_internal ? '<span class="badge badge-info">Internal</span>' : ''}
                            <span class="comment-time">${result.comment.created_at}</span>
                        </div>
                        <div class="comment-body">${result.comment.comment.replace(/\n/g, '<br>')}</div>
                    `;
                    commentsList.insertBefore(commentDiv, commentsList.firstChild);
                    
                    // Clear form
                    document.getElementById('comment-text').value = '';
                    if (document.getElementById('is-internal')) {
                        document.getElementById('is-internal').checked = false;
                    }
                } else {
                    alert('Failed to add comment: ' + (result.error || 'Unknown error'));
                }
            } catch (error) {
                alert('An error occurred. Please try again.');
            }
        });
    }

    // Assignment handling
    if (assignBtn) {
        assignBtn.addEventListener('click', function() {
            if (assignSelect.style.display === 'none') {
                assignSelect.style.display = 'block';
                assignBtn.textContent = 'Save Assignment';
                loadUsers();
            } else {
                saveAssignment();
            }
        });
    }
});

async function loadUsers() {
    // In a real application, you would fetch users from an API
    // For now, we'll use a simple approach
    const select = document.getElementById('assign-select');
    if (select.children.length <= 1) {
        // Users would be loaded from API
        // This is a placeholder
    }
}

async function saveAssignment() {
    const select = document.getElementById('assign-select');
    const userId = select.value;
    const assignBtn = document.getElementById('assign-btn');
    const assignedUser = document.getElementById('assigned-user');

    try {
        const response = await fetch(`/api/complaint/${ticketNumber}/assign/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                user_id: userId || null,
            }),
        });

        const result = await response.json();

        if (result.success) {
            location.reload();
        } else {
            alert('Failed to assign: ' + (result.error || 'Unknown error'));
        }
    } catch (error) {
        alert('An error occurred. Please try again.');
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
