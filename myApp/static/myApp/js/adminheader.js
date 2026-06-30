  // Optional: Mobile menu toggle functionality
  const mobileMenuToggle = document.getElementById('mobileMenuToggle');
  const sidebar = document.getElementById('sidebar');
  
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', function() {
      sidebar.classList.toggle('open');
    });
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(event) {
      if (window.innerWidth <= 768) {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnToggle = mobileMenuToggle.contains(event.target);
        
        if (!isClickInsideSidebar && !isClickOnToggle && sidebar.classList.contains('open')) {
          sidebar.classList.remove('open');
        }
      }
    });
  }