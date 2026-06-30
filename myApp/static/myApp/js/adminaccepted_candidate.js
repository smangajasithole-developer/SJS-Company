console.log("Admin Accepted Candidates JS Loaded");

// ============================================
// APPLICATION MODAL FUNCTIONS
// ============================================

/**
 * Opens the application modal and fetches application data
 * @param {string} applicationId - The ID of the application to view
 */
function openApplicationView(applicationId) {
    console.log("Opening admin application:", applicationId);

    const modal = document.getElementById("applicationModal");
    const applicationContent = document.getElementById("applicationContent");

    if (!modal || !applicationContent) {
        console.error("Application modal not found");
        return;
    }

    // Show modal with loading state
    modal.style.display = "block";
    applicationContent.innerHTML = `
        <div class="loading-profile">
            <i class="fas fa-spinner fa-spin"></i>
            Loading application...
        </div>
    `;

    // Fetch application data
    fetch(`/adminapplication-view/${applicationId}/`)
        .then(response => {
            console.log("Response status:", response.status);
            return response.text();
        })
        .then(html => {
            applicationContent.innerHTML = html;
        })
        .catch(error => {
            console.error("Application loading error:", error);
            applicationContent.innerHTML = `
                <div class="error-profile">
                    Failed to load application.
                </div>
            `;
        });
}

/**
 * Closes the application modal and resets content
 */
function closeApplicationView() {
    const modal = document.getElementById("applicationModal");
    const applicationContent = document.getElementById("applicationContent");

    if (modal) {
        modal.style.display = "none";
    }

    if (applicationContent) {
        applicationContent.innerHTML = `
            <div class="loading-profile">
                <i class="fas fa-spinner fa-spin"></i>
                Loading application...
            </div>
        `;
    }
}

// ============================================
// DOCUMENT VIEWER FUNCTIONS
// ============================================

/**
 * Opens the document viewer modal with a PDF
 * @param {string} url - The URL of the document to view
 * @param {string} title - The title to display in the viewer
 */
window.openDocumentViewer = function(url, title) {
    const modal = document.getElementById("documentViewerModal");
    const body = document.querySelector(".document-body");
    const titleElement = document.getElementById("documentTitle");

    if (!modal || !body || !titleElement) {
        console.error("Document viewer elements not found");
        return;
    }

    // Set document title
    titleElement.innerHTML = title;

    // Clear previous content
    body.innerHTML = "";

    // Create and configure PDF viewer
    const object = document.createElement("object");
    object.id = "documentFrame";
    object.type = "application/pdf";
    object.width = "100%";
    object.height = "700";
    object.data = window.location.origin + url;

    body.appendChild(object);
    modal.style.display = "block";
};

/**
 * Closes the document viewer modal
 */
window.closeDocumentViewer = function() {
    const modal = document.getElementById("documentViewerModal");

    if (modal) {
        modal.style.display = "none";
    }
};

// ============================================
// EVENT LISTENERS
// ============================================

/**
 * Close application modal when clicking outside
 */
window.addEventListener("click", function(event) {
    const modal = document.getElementById("applicationModal");
    if (event.target === modal) {
        closeApplicationView();
    }
});

/**
 * Close document viewer with Escape key
 */
document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        const viewerModal = document.getElementById("documentViewerModal");
        if (viewerModal && viewerModal.style.display === "block") {
            window.closeDocumentViewer();
        }

        const appModal = document.getElementById("applicationModal");
        if (appModal && appModal.style.display === "block") {
            closeApplicationView();
        }
    }
});

/**
 * Close document viewer when clicking outside
 */
window.addEventListener("click", function(event) {
    const viewerModal = document.getElementById("documentViewerModal");
    if (event.target === viewerModal) {
        window.closeDocumentViewer();
    }
});