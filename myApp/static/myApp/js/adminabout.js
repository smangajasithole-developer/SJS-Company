// Admin About Page JavaScript
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
    
    // Modal functionality for editing team members
    const modal = document.getElementById('editModal');
    const closeBtn = document.querySelector('.modal-close');
    
    window.openEditModal = function(id, name, role, bio) {
        document.getElementById('edit_member_id').value = id;
        document.getElementById('edit_name').value = name;
        document.getElementById('edit_role').value = role;
        document.getElementById('edit_bio').value = bio;
        modal.style.display = 'flex';
    };
    
    if (closeBtn) {
        closeBtn.onclick = function() {
            modal.style.display = 'none';
        };
    }
    
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
    
    // Add confirmation for delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete, .btn-delete-small');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    console.log('Admin About JS loaded');
});