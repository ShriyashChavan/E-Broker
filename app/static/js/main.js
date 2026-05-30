// Main JavaScript file for E BROKERR

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-bs-toggle="modal"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const target = button.getAttribute('data-bs-target');
            const modal = document.querySelector(target);
            if (modal) {
                modal.querySelector('.btn-danger').addEventListener('click', function() {
                    // Add loading state
                    this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Deleting...';
                    this.disabled = true;
                });
            }
        });
    });

    // Image preview for property uploads
    const imageInputs = document.querySelectorAll('input[type="file"][accept="image/*"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                // Validate file size (16MB limit)
                if (file.size > 16 * 1024 * 1024) {
                    alert('File size must be less than 16MB');
                    this.value = '';
                    return;
                }

                // Validate file type
                const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
                if (!allowedTypes.includes(file.type)) {
                    alert('Please select a valid image file (JPG, PNG, GIF)');
                    this.value = '';
                    return;
                }
            }
        });
    });

    // Search form validation
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const minRent = document.querySelector('input[name="min_rent"]').value;
            const maxRent = document.querySelector('input[name="max_rent"]').value;

            if (minRent && maxRent && parseFloat(minRent) > parseFloat(maxRent)) {
                e.preventDefault();
                alert('Minimum rent cannot be greater than maximum rent');
                return false;
            }
        });
    }

    // Rating display enhancement
    const ratingSelects = document.querySelectorAll('select[name="rating"]');
    ratingSelects.forEach(function(select) {
        select.addEventListener('change', function() {
            const value = this.value;
            const stars = '⭐'.repeat(value) + '☆'.repeat(5 - value);
            // You could add a preview here if needed
        });
    });

    // AJAX functions for dynamic updates (if needed)
    window.makeAjaxRequest = function(url, method, data, callback) {
        const xhr = new XMLHttpRequest();
        xhr.open(method, url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    callback(null, JSON.parse(xhr.responseText));
                } else {
                    callback(xhr.status, null);
                }
            }
        };

        xhr.send(JSON.stringify(data));
    };

    // Example usage for booking appointments via AJAX
    window.bookAppointment = function(propertyId) {
        if (confirm('Are you sure you want to book an appointment for this property?')) {
            makeAjaxRequest('/api/appointments/book', 'POST', { pno: propertyId }, function(err, response) {
                if (err) {
                    alert('Error booking appointment. Please try again.');
                } else {
                    alert('Appointment booked successfully!');
                    location.reload();
                }
            });
        }
    };

    // Example usage for submitting feedback via AJAX
    window.submitFeedback = function(propertyId, rating, comment) {
        makeAjaxRequest('/api/feedback/add', 'POST', {
            pno: propertyId,
            rating: rating,
            comment: comment
        }, function(err, response) {
            if (err) {
                alert('Error submitting feedback. Please try again.');
            } else {
                alert('Feedback submitted successfully!');
                location.reload();
            }
        });
    };
});

// Utility functions
window.escapeHtml = function(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
};

window.formatCurrency = function(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
};

window.formatDate = function(dateString) {
    return new Date(dateString).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};