// Create Complaint JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const complaintForm = document.getElementById('complaintForm');
    const errorMessage = document.getElementById('errorMessage');

    if (complaintForm) {
        complaintForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(complaintForm);

            try {
                // Ensure category is empty string if not selected
                const categorySelect = document.getElementById('category');
                if (categorySelect && !categorySelect.value) {
                    formData.set('category', '');
                }

                const response = await fetch('/complaint/create/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: formData,
                });

                // Check if response is ok
                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('Server error response:', errorText);
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                let result;
                try {
                    result = await response.json();
                } catch (jsonError) {
                    const text = await response.text();
                    console.error('Failed to parse JSON response:', text);
                    showError('errorMessage', 'Server returned an invalid response. Please try again.');
                    return;
                }

                if (result.success) {
                    window.location.href = result.redirect || `/complaint/${result.ticket_number}/`;
                } else {
                    let errorText = 'Failed to create complaint. ';
                    if (result.errors) {
                        const errorMessages = [];
                        for (const field in result.errors) {
                            if (Array.isArray(result.errors[field])) {
                                result.errors[field].forEach(msg => {
                                    errorMessages.push(`${field}: ${msg.message || msg}`);
                                });
                            } else if (typeof result.errors[field] === 'object') {
                                result.errors[field].forEach(msg => {
                                    errorMessages.push(`${field}: ${msg.message || msg}`);
                                });
                            } else {
                                errorMessages.push(`${field}: ${result.errors[field]}`);
                            }
                        }
                        errorText += errorMessages.join(' ');
                    } else if (result.error) {
                        errorText += result.error;
                    }
                    showError('errorMessage', errorText);
                    console.error('Form errors:', result);
                }
            } catch (error) {
                console.error('Error submitting form:', error);
                showError('errorMessage', 'An error occurred. Please check the console for details.');
            }
        });
    }
});

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

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        // Scroll to error message
        errorElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } else {
        // Fallback: show alert if element not found
        alert(message);
    }
}
