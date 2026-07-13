// ============================================================
// FORGOT PASSWORD PAGE JAVASCRIPT
// ============================================================

// ============================================================
// AUTO-DISMISS MESSAGES
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');
    
    messages.forEach((message, index) => {
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px) scale(0.95)';
            message.style.transition = 'all 0.3s ease';
            setTimeout(() => {
                if (message.parentNode) {
                    message.remove();
                }
            }, 300);
        }, 5000 + (index * 300));
    });
});

// ============================================================
// FORM VALIDATION (Client-side)
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('forgotPasswordForm');
    const emailInput = document.getElementById('email');
    const submitBtn = document.getElementById('submitBtn');

    if (form) {
        // Remove error on focus
        emailInput.addEventListener('focus', function() {
            this.classList.remove('error');
            this.style.borderColor = '';
            this.style.boxShadow = '';
            const err = this.closest('.form-group').querySelector('.field-error');
            if (err) err.remove();
        });

        // Real-time validation
        emailInput.addEventListener('blur', function() {
            const email = this.value.trim();
            if (email && !isValidEmail(email)) {
                showFieldError(this, 'Please enter a valid email address');
            } else {
                this.classList.remove('error');
                this.style.borderColor = '';
                this.style.boxShadow = '';
                const err = this.closest('.form-group').querySelector('.field-error');
                if (err) err.remove();
            }
        });

        form.addEventListener('submit', function(e) {
            let hasError = false;
            
            // Remove existing errors
            document.querySelectorAll('.field-error').forEach(el => el.remove());
            document.querySelectorAll('.form-control.error').forEach(el => {
                el.classList.remove('error');
                el.style.borderColor = '';
                el.style.boxShadow = '';
            });

            // Validate email
            const email = emailInput.value.trim();
            if (!email) {
                e.preventDefault();
                showFieldError(emailInput, 'Please enter your email address');
                hasError = true;
            } else if (!isValidEmail(email)) {
                e.preventDefault();
                showFieldError(emailInput, 'Please enter a valid email address');
                hasError = true;
            }

            // If no errors, show loading state
            if (!hasError) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.7';
            }
        });
    }
});

// ============================================================
// HELPER FUNCTIONS
// ============================================================

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Show field error
 */
function showFieldError(field, message) {
    // Highlight field
    field.classList.add('error');
    field.style.borderColor = '#dc2626';
    field.style.boxShadow = '0 0 0 4px rgba(220, 38, 38, 0.1)';

    // Remove existing error
    const existingError = field.closest('.form-group').querySelector('.field-error');
    if (existingError) existingError.remove();

    // Create error message
    const errorEl = document.createElement('span');
    errorEl.className = 'field-error';
    errorEl.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    field.closest('.form-group').appendChild(errorEl);

    // Focus the field
    field.focus();
}

// ============================================================
// PREVENT MULTIPLE SUBMISSIONS
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('forgotPasswordForm');
    
    if (form) {
        form.addEventListener('submit', function() {
            const submitBtn = document.getElementById('submitBtn');
            if (submitBtn.disabled) {
                return false;
            }
        });
    }
});