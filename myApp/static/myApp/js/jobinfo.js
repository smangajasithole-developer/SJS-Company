// ============================================================
// JOBINFO.JS - Job Information Page Interactions
// ============================================================

document.addEventListener('DOMContentLoaded', function() {

    // ==========================================================
    // AUTO-DISMISS ALERTS
    // ==========================================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });

    // ==========================================================
    // APPLY BUTTON HOVER EFFECTS
    // ==========================================================
    const applyButtons = document.querySelectorAll('.apply-btn:not(.applied-btn)');
    applyButtons.forEach(function(btn) {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 8px 25px rgba(243, 156, 18, 0.3)';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 15px rgba(243, 156, 18, 0.2)';
        });
    });

    // ==========================================================
    // CONTENT BLOCK EXPAND/COLLAPSE
    // ==========================================================
    const contentBlocks = document.querySelectorAll('.content-block');
    const descriptionSection = document.querySelector('.job-description');

    if (contentBlocks.length > 3 && descriptionSection) {
        // Hide blocks beyond the first 3
        contentBlocks.forEach(function(block, index) {
            if (index > 2) {
                block.style.display = 'none';
            }
        });

        // Create "View More" button
        const showMoreBtn = document.createElement('button');
        showMoreBtn.className = 'btn-more';
        showMoreBtn.innerHTML = '<i class="fas fa-chevron-down"></i> View More';
        showMoreBtn.setAttribute('aria-expanded', 'false');
        descriptionSection.appendChild(showMoreBtn);

        // Toggle functionality
        showMoreBtn.addEventListener('click', function() {
            const hiddenBlocks = descriptionSection.querySelectorAll('.content-block');
            const isExpanded = this.getAttribute('aria-expanded') === 'true';

            if (isExpanded) {
                // Collapse
                hiddenBlocks.forEach(function(block, index) {
                    if (index > 2) {
                        block.style.display = 'none';
                    }
                });
                this.innerHTML = '<i class="fas fa-chevron-down"></i> View More';
                this.setAttribute('aria-expanded', 'false');
            } else {
                // Expand
                hiddenBlocks.forEach(function(block) {
                    block.style.display = 'block';
                });
                this.innerHTML = '<i class="fas fa-chevron-up"></i> Show Less';
                this.setAttribute('aria-expanded', 'true');
            }
        });
    }

    // ==========================================================
    // JOB META ITEMS - ADD TOOLTIPS FOR LONG TEXT
    // ==========================================================
    const metaItems = document.querySelectorAll('.meta-item');
    metaItems.forEach(function(item) {
        const text = item.textContent.trim();
        if (text.length > 30) {
            item.setAttribute('title', text);
        }
    });

    // ==========================================================
    // KEYBOARD NAVIGATION FOR INTERACTIVE ELEMENTS
    // ==========================================================
    const interactiveElements = document.querySelectorAll('.apply-btn, .btn-more, .user-circle');
    interactiveElements.forEach(function(el) {
        el.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        // Make focusable
        if (!el.getAttribute('tabindex')) {
            el.setAttribute('tabindex', '0');
        }
    });

    // ==========================================================
    // RESPONSIVE BEHAVIOR - ADJUST LAYOUT ON RESIZE
    // ==========================================================
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            const jobMeta = document.querySelector('.job-meta');
            if (jobMeta) {
                const items = jobMeta.querySelectorAll('.meta-item');
                const windowWidth = window.innerWidth;
                
                if (windowWidth < 768) {
                    items.forEach(function(item) {
                        item.style.display = 'block';
                        item.style.marginBottom = '0.5rem';
                    });
                } else {
                    items.forEach(function(item) {
                        item.style.display = 'inline-block';
                        item.style.marginBottom = '0';
                    });
                }
            }
        }, 250);
    });

});

// ============================================================
// USER MENU TOGGLE (Global Function)
// ============================================================
function toggleUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    const userCircle = document.querySelector('.user-circle');
    
    if (dropdown) {
        const isExpanded = dropdown.classList.contains('show');
        dropdown.classList.toggle('show');
        if (userCircle) {
            userCircle.setAttribute('aria-expanded', !isExpanded);
        }
    }
}

// ============================================================
// CLOSE DROPDOWN WHEN CLICKING OUTSIDE
// ============================================================
document.addEventListener('click', function(event) {
    const userMenu = document.querySelector('.user-menu');
    const dropdown = document.getElementById('userDropdown');
    
    if (userMenu && dropdown) {
        if (!userMenu.contains(event.target)) {
            dropdown.classList.remove('show');
            const userCircle = userMenu.querySelector('.user-circle');
            if (userCircle) {
                userCircle.setAttribute('aria-expanded', 'false');
            }
        }
    }
});

// ============================================================
// CLOSE DROPDOWN WITH ESC KEY
// ============================================================
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const dropdown = document.getElementById('userDropdown');
        if (dropdown && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
            const userCircle = document.querySelector('.user-circle');
            if (userCircle) {
                userCircle.setAttribute('aria-expanded', 'false');
                userCircle.focus();
            }
        }
    }
});

// ============================================================
// SMOOTH SCROLL FOR JOB DESCRIPTION LINKS (if any)
// ============================================================
document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});