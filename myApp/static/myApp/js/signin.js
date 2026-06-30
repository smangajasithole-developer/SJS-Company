// ============================================================
// SIGN IN PAGE JAVASCRIPT
// ============================================================

// ============================================================
// PASSWORD TOGGLE
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const wrapper = this.closest('.password-input-wrapper');
            const passwordField = wrapper.querySelector('.form-control');
            
            if (passwordField) {
                const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordField.setAttribute('type', type);
                
                // Toggle icon
                const icon = this.querySelector('i');
                if (icon) {
                    icon.classList.toggle('fa-eye');
                    icon.classList.toggle('fa-eye-slash');
                }
            }
        });
    });
});

// ============================================================
// AUTO-DISMISS MESSAGES (FIXED)
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');
    
    messages.forEach((message, index) => {
        // Add close button functionality
        const closeBtn = message.querySelector('.message-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.style.opacity = '0';
                message.style.transform = 'translateY(-10px) scale(0.95)';
                message.style.transition = 'all 0.3s ease';
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }
        
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
        }, 30000 + (index * 300));
    });
});

// ============================================================
// FORM VALIDATION (Client-side)
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.signin-form');
    
    if (form) {
        // Remove error on focus for all fields
        const inputs = form.querySelectorAll('.form-control');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.classList.remove('error');
                this.style.borderColor = '';
                this.style.boxShadow = '';
                const err = this.parentElement.querySelector('.field-error');
                if (err) err.remove();
            });
        });
        
        form.addEventListener('submit', function(e) {
            let hasError = false;
            const username = document.getElementById('username');
            const password = document.getElementById('password');
            
            // Remove existing errors
            document.querySelectorAll('.field-error').forEach(el => el.remove());
            document.querySelectorAll('.form-control.error').forEach(el => {
                el.classList.remove('error');
                el.style.borderColor = '';
                el.style.boxShadow = '';
            });
            
            if (username && username.value.trim() === '') {
                e.preventDefault();
                showFieldError(username, 'Please enter your username');
                hasError = true;
            }
            
            if (password && password.value.trim() === '') {
                e.preventDefault();
                showFieldError(password, 'Please enter your password');
                hasError = true;
            }
            
            // If no errors, show loading state
            if (!hasError) {
                const btn = form.querySelector('.btn-signin');
                if (btn) {
                    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing in...';
                    btn.disabled = true;
                }
            }
        });
    }
});

// ============================================================
// FIELD ERROR HELPERS (FIXED)
// ============================================================
function showFieldError(field, message) {
    // Highlight field
    field.classList.add('error');
    field.style.borderColor = '#dc2626';
    field.style.boxShadow = '0 0 0 4px rgba(220, 38, 38, 0.1)';
    
    // Remove existing error if any
    const existingError = field.parentElement.querySelector('.field-error');
    if (existingError) existingError.remove();
    
    // Create error message
    const errorEl = document.createElement('span');
    errorEl.className = 'field-error';
    errorEl.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    field.parentElement.appendChild(errorEl);
    
    // Focus the field
    field.focus();
}