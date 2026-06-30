// ============================================================
// HR APPLICATIONS – JavaScript (hrapplications.js)
// Handles modal interactions, application fetching, document viewing, and UI updates.
// Data logic remains untouched.
// ============================================================

console.log("HR Applications JS Loaded");

// ============================================================
// APPLICATION VIEW MODAL
// ============================================================

/**
 * Opens the application view modal and fetches application data
 * @param {string|number} applicationId - The ID of the application
 * @param {string} [source] - Optional source parameter for tracking
 */
function openApplicationView(applicationId, source) {
    console.log("Opening application:", applicationId);
    if (source) {
        console.log("Source:", source);
    }

    // Get modal elements
    const modal = document.getElementById("applicationModal");
    const applicationContent = document.getElementById("applicationContent");

    // Validate elements exist
    if (!modal || !applicationContent) {
        console.error("Modal elements missing");
        return;
    }

    // Show modal
    modal.style.display = "block";
    document.body.style.overflow = "hidden"; // Prevent body scroll

    // Show loading state
    applicationContent.innerHTML = `
        <div class="loading-profile">
            <i class="fas fa-spinner fa-spin"></i>
            Loading application...
        </div>
    `;

    // Build the fetch URL
    let url = `/hrapplication-view/${applicationId}/`;
    if (source) {
        url += `?source=${source}`;
    } else {
        url += `?source=hrapplications`;
    }

    // Fetch application data via AJAX
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            applicationContent.innerHTML = html;
            // Re-initialize any dynamic elements if needed
        })
        .catch(error => {
            console.error("Error loading application:", error);
            applicationContent.innerHTML = `
                <div class="error-profile">
                    <i class="fas fa-exclamation-circle"></i>
                    Failed to load application. Please try again.
                </div>
            `;
        });
}

/**
 * Closes the application view modal
 */
function closeApplicationView() {
    const modal = document.getElementById("applicationModal");
    const applicationContent = document.getElementById("applicationContent");

    if (modal) {
        modal.style.display = "none";
        document.body.style.overflow = ""; // Restore body scroll
    }

    // Reset content to loading state for next open
    if (applicationContent) {
        applicationContent.innerHTML = `
            <div class="loading-profile">
                <i class="fas fa-spinner fa-spin"></i>
                Loading application...
            </div>
        `;
    }
}

// ============================================================
// DOCUMENT VIEWER MODAL
// ============================================================

/**
 * Opens the document viewer modal with the specified document
 * @param {string} documentUrl - The URL of the document to view
 * @param {string} documentName - The name/title of the document
 */
function openDocumentViewer(documentUrl, documentName) {
    console.log("Opening document:", documentName);

    const modal = document.getElementById("documentViewerModal");
    const body = document.querySelector(".document-body");
    const title = document.getElementById("documentTitle");

    if (!modal || !body || !title) {
        console.error("Document viewer elements missing");
        return;
    }

    title.textContent = documentName || "Document Viewer";

    // Completely remove previous viewer
    body.innerHTML = "";

    // Create a brand new iframe every time
    const iframe = document.createElement("iframe");

    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.border = "none";

    const fullUrl = documentUrl.startsWith("http")
        ? documentUrl
        : window.location.origin + documentUrl;

    // Cache buster
    iframe.src =
        fullUrl +
        (fullUrl.includes("?") ? "&" : "?") +
        "_=" +
        new Date().getTime();

    body.appendChild(iframe);

    modal.style.display = "block";
    document.body.style.overflow = "hidden";
}

// ============================================================
// CLOSE MODALS ON OUTSIDE CLICK
// ============================================================
function closeDocumentViewer() {
    const modal = document.getElementById("documentViewerModal");
    const body = document.querySelector(".document-body");

    if (modal) {
        modal.style.display = "none";
    }

    if (body) {
        body.innerHTML = "";
    }

    document.body.style.overflow = "";
}

// ============================================================
// CLOSE MODALS WITH ESCAPE KEY
// ============================================================
document.addEventListener("DOMContentLoaded", function() {
    document.addEventListener("keydown", function(event) {
        if (event.key === "Escape") {
            // Close application modal if open
            const appModal = document.getElementById("applicationModal");
            if (appModal && appModal.style.display === "block") {
                closeApplicationView();
            }

            // Close document viewer modal if open
            const docModal = document.getElementById("documentViewerModal");
            if (docModal && docModal.style.display === "block") {
                closeDocumentViewer();
            }
        }
    });

    // ============================================================
    // TABLE ROW INTERACTIONS
    // ============================================================
    const viewButtons = document.querySelectorAll(".view-application-btn");
    viewButtons.forEach(button => {
        button.addEventListener("mouseenter", function() {
            this.style.transform = "translateY(-1px)";
        });
        button.addEventListener("mouseleave", function() {
            this.style.transform = "translateY(0)";
        });
    });

    // ============================================================
    // DECISION BUTTON CONFIRMATION
    // ============================================================
    const acceptButtons = document.querySelectorAll(".btn-accept");
    const rejectButtons = document.querySelectorAll(".btn-reject");

    acceptButtons.forEach(button => {
        button.addEventListener("click", function(e) {
            if (!confirm("Are you sure you want to ACCEPT this candidate?")) {
                e.preventDefault();
            }
        });
    });

    rejectButtons.forEach(button => {
        button.addEventListener("click", function(e) {
            if (!confirm("Are you sure you want to REJECT this candidate?")) {
                e.preventDefault();
            }
        });
    });
});

// ============================================================
// EXPOSE FUNCTIONS TO GLOBAL SCOPE (for inline onclick)
// ============================================================
window.openApplicationView = openApplicationView;
window.closeApplicationView = closeApplicationView;
window.openDocumentViewer = openDocumentViewer;
window.closeDocumentViewer = closeDocumentViewer;