// Optional: Mobile menu toggle functionality
// This is only for responsive behavior on mobile devices

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on mobile
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
    // Add mobile menu toggle button
    function addMobileToggle() {
        if (!isMobile()) return;
        if (document.querySelector('.mobile-toggle')) return;
        
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'mobile-toggle';
        toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
        toggleBtn.style.cssText = `
            position: fixed;
            top: 72px;
            left: 15px;
            z-index: 1001;
            background: #1a3a5c;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 12px;
            cursor: pointer;
            font-size: 1.2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        `;
        
        toggleBtn.onclick = function() {
            const sidebar = document.querySelector('.sidebar');
            sidebar.classList.toggle('open');
        };
        
        document.body.appendChild(toggleBtn);
    }
    
    // Remove mobile toggle on desktop
    function removeMobileToggle() {
        const toggle = document.querySelector('.mobile-toggle');
        if (toggle) toggle.remove();
    }
    
    // Handle window resize
    function handleResize() {
        if (isMobile()) {
            addMobileToggle();
        } else {
            removeMobileToggle();
            const sidebar = document.querySelector('.sidebar');
            if (sidebar) sidebar.classList.remove('open');
        }
    }
    
    // Initialize
    handleResize();
    window.addEventListener('resize', handleResize);
});