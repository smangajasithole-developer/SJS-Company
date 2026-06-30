// ============================================================
// SIGN UP PAGE JAVASCRIPT
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
// PASSWORD STRENGTH METER
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('password');
    const strengthBars = document.querySelectorAll('.strength-bar');
    const strengthText = document.querySelector('.strength-text');
    
    if (passwordField && strengthBars.length > 0) {
        passwordField.addEventListener('input', function() {
            const password = this.value;
            const strength = checkPasswordStrength(password);
            
            // Update bars
            strengthBars.forEach((bar, index) => {
                bar.classList.remove('active', 'weak', 'medium', 'strong');
                if (index < strength.score) {
                    bar.classList.add('active', strength.class);
                }
            });
            
            // Update text
            if (strengthText) {
                strengthText.textContent = password.length > 0 ? strength.label : 'Password strength';
                strengthText.style.color = password.length > 0 ? strength.color : '#8a9bb5';
            }
        });
    }
});

function checkPasswordStrength(password) {
    let score = 0;
    
    if (password.length === 0) {
        return { score: 0, label: 'Password strength', class: '', color: '#8a9bb5' };
    }
    
    // Length check
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    
    // Complexity checks
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[^a-zA-Z0-9]/.test(password)) score++;
    
    // Cap at 5
    score = Math.min(score, 5);
    
    const strengthMap = {
        0: { label: 'Very Weak', class: 'weak', color: '#dc2626' },
        1: { label: 'Weak', class: 'weak', color: '#dc2626' },
        2: { label: 'Fair', class: 'weak', color: '#f59e0b' },
        3: { label: 'Good', class: 'medium', color: '#f59e0b' },
        4: { label: 'Strong', class: 'strong', color: '#16a34a' },
        5: { label: 'Very Strong', class: 'strong', color: '#16a34a' }
    };
    
    return {
        score: score,
        label: strengthMap[score].label,
        class: strengthMap[score].class,
        color: strengthMap[score].color
    };
}

// ============================================================
// PASSWORD MATCH VALIDATION
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('password');
    const confirmField = document.getElementById('confirm_password');
    const matchDisplay = document.getElementById('passwordMatch');
    
    function checkMatch() {
        if (!passwordField || !confirmField || !matchDisplay) return;
        
        const password = passwordField.value;
        const confirm = confirmField.value;
        
        if (confirm.length === 0) {
            matchDisplay.textContent = '';
            matchDisplay.className = 'password-match';
            confirmField.classList.remove('error', 'success');
            return;
        }
        
        if (password === confirm) {
            matchDisplay.innerHTML = '<i class="fas fa-check-circle"></i> Passwords match';
            matchDisplay.className = 'password-match match';
            confirmField.classList.remove('error');
            confirmField.classList.add('success');
        } else {
            matchDisplay.innerHTML = '<i class="fas fa-exclamation-circle"></i> Passwords do not match';
            matchDisplay.className = 'password-match no-match';
            confirmField.classList.remove('success');
            confirmField.classList.add('error');
        }
    }
    
    if (passwordField && confirmField) {
        passwordField.addEventListener('input', checkMatch);
        confirmField.addEventListener('input', checkMatch);
    }
});

// ============================================================
// FORM VALIDATION
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.signup-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const password = document.getElementById('password');
            const confirm = document.getElementById('confirm_password');
            const terms = document.getElementById('terms');
            
            let hasError = false;
            
            // Validate password match
            if (password && confirm && password.value !== confirm.value) {
                e.preventDefault();
                showFieldError(confirm, 'Passwords do not match');
                hasError = true;
            }
            
            // Validate password strength
            if (password && password.value.length < 8) {
                e.preventDefault();
                showFieldError(password, 'Password must be at least 8 characters');
                hasError = true;
            }
            
            // Validate terms
            if (terms && !terms.checked) {
                e.preventDefault();
                const termsGroup = terms.closest('.terms-group');
                if (termsGroup) {
                    const errorEl = termsGroup.querySelector('.field-error');
                    if (!errorEl) {
                        const err = document.createElement('span');
                        err.className = 'field-error';
                        err.style.cssText = `
                            color: #dc2626;
                            font-size: 0.8rem;
                            margin-top: 0.25rem;
                            display: flex;
                            align-items: center;
                            gap: 0.3rem;
                        `;
                        err.innerHTML = '<i class="fas fa-exclamation-circle"></i> You must agree to the terms';
                        termsGroup.appendChild(err);
                    }
                }
                hasError = true;
            }
            
            if (hasError) {
                // Scroll to first error
                const firstError = document.querySelector('.error, .field-error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    }
});

// ============================================================
// FIELD ERROR HELPERS
// ============================================================
function showFieldError(field, message) {
    field.classList.add('error');
    
    let errorEl = field.parentElement.querySelector('.field-error');
    if (!errorEl) {
        errorEl = document.createElement('span');
        errorEl.className = 'field-error';
        errorEl.style.cssText = `
            color: #dc2626;
            font-size: 0.8rem;
            margin-top: 0.25rem;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        `;
        field.parentElement.appendChild(errorEl);
    }
    errorEl.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    
    field.addEventListener('focus', function() {
        this.classList.remove('error');
        const err = this.parentElement.querySelector('.field-error');
        if (err) err.remove();
    }, { once: true });
}

// ============================================================
// AUTO-DISMISS MESSAGES
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');
    
    messages.forEach((message, index) => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        }, 5000 + (index * 500));
    });
});