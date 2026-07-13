// ============================================================
// RESET PASSWORD PAGE JAVASCRIPT
// ============================================================

// ============================================================
// PASSWORD TOGGLE
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordField = document.getElementById(targetId);
            
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
// AUTO-DISMISS MESSAGES
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
        }, 5000 + (index * 300));
    });
});

// ============================================================
// PASSWORD VALIDATION & STRENGTH
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirm_password');
    const submitBtn = document.getElementById('submitBtn');
    const form = document.getElementById('resetPasswordForm');
    
    if (passwordInput) {
        // Real-time password validation
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            validatePassword(password);
            checkPasswordMatch();
        });
        
        // Remove error on focus
        passwordInput.addEventListener('focus', function() {
            this.classList.remove('error');
            this.style.borderColor = '';
            this.style.boxShadow = '';
            const err = this.closest('.form-group').querySelector('.field-error');
            if (err) err.remove();
        });
    }
    
    if (confirmInput) {
        confirmInput.addEventListener('input', function() {
            checkPasswordMatch();
        });
        
        confirmInput.addEventListener('focus', function() {
            this.classList.remove('error');
            this.style.borderColor = '';
            this.style.boxShadow = '';
            const err = this.closest('.form-group').querySelector('.field-error');
            if (err) err.remove();
        });
    }
    
    // Form submission
    if (form) {
        form.addEventListener('submit', function(e) {
            let hasError = false;
            
            // Remove existing errors
            document.querySelectorAll('.field-error').forEach(el => el.remove());
            document.querySelectorAll('.form-control.error').forEach(el => {
                el.classList.remove('error');
                el.style.borderColor = '';
                el.style.boxShadow = '';
            });
            
            // Validate password
            const password = passwordInput.value;
            const passwordValid = validatePassword(password, true);
            
            if (!password) {
                e.preventDefault();
                showFieldError(passwordInput, 'Please enter a new password');
                hasError = true;
            } else if (!passwordValid) {
                e.preventDefault();
                showFieldError(passwordInput, 'Password does not meet requirements');
                hasError = true;
            }
            
            // Validate confirm password
            const confirm = confirmInput.value;
            if (!confirm) {
                e.preventDefault();
                showFieldError(confirmInput, 'Please confirm your password');
                hasError = true;
            } else if (password !== confirm) {
                e.preventDefault();
                showFieldError(confirmInput, 'Passwords do not match');
                hasError = true;
            }
            
            // If no errors, show loading state
            if (!hasError) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Updating...';
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.7';
            }
        });
    }
});

// ============================================================
// PASSWORD VALIDATION FUNCTIONS
// ============================================================
function validatePassword(password, showErrors = false) {
    const requirements = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };
    
    // Update requirement indicators
    const requirementElements = document.querySelectorAll('.requirement');
    requirementElements.forEach(el => {
        const reqType = el.getAttribute('data-requirement');
        const icon = el.querySelector('i');
        const isMet = requirements[reqType] || false;
        
        if (isMet) {
            el.classList.add('met');
            el.classList.remove('unmet');
            icon.className = 'fas fa-check-circle';
        } else {
            el.classList.add('unmet');
            el.classList.remove('met');
            icon.className = 'fas fa-circle';
        }
    });
    
    // Update strength meter
    updateStrengthMeter(password);
    
    // Return overall validity
    return Object.values(requirements).every(Boolean);
}

// ============================================================
// PASSWORD STRENGTH METER
// ============================================================
function updateStrengthMeter(password) {
    const bar = document.getElementById('strengthBar');
    const text = document.getElementById('strengthText');
    
    if (!bar || !text) return;
    
    let score = 0;
    
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[a-z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score++;
    
    let strength = 'weak';
    let strengthText = 'Weak';
    
    if (score >= 6) {
        strength = 'strong';
        strengthText = 'Strong';
    } else if (score >= 4) {
        strength = 'good';
        strengthText = 'Good';
    } else if (score >= 3) {
        strength = 'fair';
        strengthText = 'Fair';
    } else {
        strength = 'weak';
        strengthText = 'Weak';
    }
    
    // Update bar
    bar.className = 'strength-meter-bar';
    bar.classList.add(strength);
    
    // Update text
    text.className = 'strength-text';
    text.classList.add(strength);
    text.textContent = `Password strength: ${strengthText}`;
}

// ============================================================
// PASSWORD MATCH CHECK
// ============================================================
function checkPasswordMatch() {
    const password = document.getElementById('password');
    const confirm = document.getElementById('confirm_password');
    const status = document.getElementById('matchStatus');
    
    if (!password || !confirm || !status) return;
    
    const passVal = password.value;
    const confirmVal = confirm.value;
    
    if (!passVal || !confirmVal) {
        status.textContent = '';
        status.className = 'password-match-status';
        return;
    }
    
    if (passVal === confirmVal) {
        status.textContent = '✓ Passwords match';
        status.className = 'password-match-status match';
        confirm.classList.add('success');
        confirm.classList.remove('error');
    } else {
        status.textContent = '✗ Passwords do not match';
        status.className = 'password-match-status no-match';
        confirm.classList.add('error');
        confirm.classList.remove('success');
    }
}

// ============================================================
// FIELD ERROR HELPER
// ============================================================
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