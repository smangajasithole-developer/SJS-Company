// Admin Services Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Mobile menu toggle functionality
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
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
            document.querySelector('.sidebar').classList.toggle('open');
        };
        
        document.body.appendChild(toggleBtn);
    }
    
    function removeMobileToggle() {
        const toggle = document.querySelector('.mobile-toggle');
        if (toggle) toggle.remove();
    }
    
    function handleResize() {
        if (isMobile()) {
            addMobileToggle();
        } else {
            removeMobileToggle();
            const sidebar = document.querySelector('.sidebar');
            if (sidebar) sidebar.classList.remove('open');
        }
    }
    
    handleResize();
    window.addEventListener('resize', handleResize);
    
    // Toggle edit form visibility
    window.toggleEdit = function(id) {
        const row = document.getElementById("edit-form-" + id);
        if (row) {
            row.style.display = row.style.display === "none" ? "table-row" : "none";
        }
    };
    
    // Add confirmation for delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete-small');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const form = this.closest('form');
            if (form && !confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    console.log('Admin Services JS loaded');
});