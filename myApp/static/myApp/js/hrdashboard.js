// ============================================================
// HR DASHBOARD – JavaScript (hrdashboard.js)
// Data logic kept intact – only UI / interaction helpers.
// ============================================================

document.addEventListener('DOMContentLoaded', function () {

    // ------------------------------------------------------------
    // 1. SIDEBAR TOGGLE (for mobile / small screens)
    //    Adds a toggle button to the top‑bar if it doesn't exist,
    //    so the sidebar can be shown/hidden on narrow viewports.
    // ------------------------------------------------------------
    const sidebar = document.querySelector('.sidebar');
    const topbarRight = document.querySelector('.topbar-right');

    // Only inject toggle if sidebar exists and we are on small screen
    if (sidebar && topbarRight) {
        // Check if toggle already exists (avoid duplicates)
        let toggleBtn = document.getElementById('sidebarToggle');
        if (!toggleBtn) {
            toggleBtn = document.createElement('button');
            toggleBtn.id = 'sidebarToggle';
            toggleBtn.setAttribute('aria-label', 'Toggle sidebar');
            toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
            toggleBtn.style.cssText = `
                background: transparent;
                border: none;
                font-size: 1.3rem;
                color: #1e3a5f;
                cursor: pointer;
                padding: 0 0.5rem;
                display: none;  /* hidden by default, shown via media query in CSS */
            `;
            // Insert toggle before the right content
            topbarRight.parentNode.insertBefore(toggleBtn, topbarRight);
        }

        // Toggle click handler
        toggleBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            if (sidebar.style.display === 'none' || sidebar.style.display === '') {
                sidebar.style.display = 'flex';
                sidebar.style.flexDirection = 'column'; // restore
            } else {
                sidebar.style.display = 'none';
            }
        });

        // If window resizes beyond mobile, ensure sidebar is visible
        function handleResize() {
            if (window.innerWidth > 640) {
                sidebar.style.display = 'flex';
                sidebar.style.flexDirection = 'column';
                // hide toggle on wide screens
                toggleBtn.style.display = 'none';
            } else {
                // show toggle on small screens
                toggleBtn.style.display = 'inline-block';
                // if sidebar was hidden by user, keep it hidden, otherwise show
                // but we do NOT force display:flex here to respect user toggle.
                // However, if sidebar was never hidden, we want it visible by default.
                // So we check if it's not explicitly hidden.
                if (sidebar.style.display !== 'none') {
                    sidebar.style.display = 'flex';
                    sidebar.style.flexDirection = 'row';
                    sidebar.style.flexWrap = 'wrap';
                }
            }
        }

        // initial call
        handleResize();
        window.addEventListener('resize', handleResize);
    }

    // ------------------------------------------------------------
    // 2. ACTIVE LINK – highlight current page (already handled by
    //    Django template with 'active' class, but we keep a small
    //    fallback in case of dynamic changes).
    // ------------------------------------------------------------
    const currentUrl = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar a');

    sidebarLinks.forEach(link => {
        // if the link's href matches current path (exact or starts with)
        // we keep the 'active' class logic from server, but we also
        // ensure only one active at a time (just in case).
        // This is a client-side safety net – server-side active class is primary.
        const linkHref = link.getAttribute('href');
        if (linkHref && linkHref !== '#' && linkHref !== '') {
            // remove active from all if we want to re-evaluate (but we trust server)
            // Actually we do nothing – the server already sets active class.
            // But if you need to override, you can uncomment:
            // if (currentUrl === linkHref || currentUrl.startsWith(linkHref + '?')) {
            //     link.classList.add('active');
            // } else {
            //     link.classList.remove('active');
            // }
        }
    });

    // ------------------------------------------------------------
    // 3. CLOSE SIDEBAR ON LINK CLICK (mobile UX)
    //    When a link is clicked on small screens, auto‑close sidebar.
    // ------------------------------------------------------------
    if (sidebar) {
        const links = sidebar.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', function () {
                // only on small screens (width <= 640px)
                if (window.innerWidth <= 640) {
                    const toggle = document.getElementById('sidebarToggle');
                    // if sidebar is visible and toggle exists, close it
                    if (toggle && sidebar.style.display !== 'none') {
                        sidebar.style.display = 'none';
                    }
                }
            });
        });
    }

    // ------------------------------------------------------------
    // 4. (Optional) keep data logic intact – we don't touch any
    //    server-rendered data, only UI enhancements.
    // ------------------------------------------------------------
    console.log('HR Dashboard JS loaded – data logic untouched.');

});