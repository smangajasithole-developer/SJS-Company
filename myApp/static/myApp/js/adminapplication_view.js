console.log("Admin Accepted Candidates JS Loaded");

// ============================================
// APPLICATION MODAL FUNCTIONS
// ============================================

function openApplicationView(applicationId) {
    console.log("Opening application:", applicationId);

    const modal = document.getElementById("applicationModal");
    const applicationContent = document.getElementById("applicationContent");

    modal.style.display = "block";

    applicationContent.innerHTML = `
        <div class="loading-profile">
            <i class="fas fa-spinner fa-spin"></i>
            Loading application...
        </div>
    `;

    fetch(`/adminapplication-view/${applicationId}/`)
        .then(response => {
            console.log("Response status:", response.status);
            return response.text();
        })
        .then(html => {
            console.log(html);
            applicationContent.innerHTML = html;
        })
        .catch(error => {
            console.error("ERROR:", error);
            applicationContent.innerHTML = `
                <div class="error-profile">
                    ${error}
                </div>
            `;
        });
}

function closeApplicationView() {
    const modal = document.getElementById("applicationModal");

    if (modal) {
        modal.style.display = "none";
    }
}

// ============================================
// DOCUMENT VIEWER FUNCTIONS
// ============================================

let currentDocumentFrame = null;

function openDocumentViewer(url, title) {

    console.log("Opening:", title);
    console.log("URL:", url);

    const modal = document.getElementById("documentViewerModal");
    const body = document.querySelector(".document-body");
    const titleElement = document.getElementById("documentTitle");

    if (!modal || !body || !titleElement) {
        console.error("Document viewer elements not found.");
        return;
    }

    // Update title
    titleElement.textContent = title || "Document Viewer";

    // Remove previous iframe completely
    if (currentDocumentFrame) {
        currentDocumentFrame.src = "about:blank";
        currentDocumentFrame.remove();
        currentDocumentFrame = null;
    }

    // Empty container
    body.innerHTML = "";

    // Force a unique URL every time
    const separator = url.includes("?") ? "&" : "?";
    const viewerUrl = `${url}${separator}v=${Date.now()}_${Math.random()}`;

    // Create a brand new iframe
    const iframe = document.createElement("iframe");

    iframe.id = "documentFrame";
    iframe.src = viewerUrl;
    iframe.width = "100%";
    iframe.height = "100%";
    iframe.style.border = "0";
    iframe.setAttribute("loading", "eager");

    body.appendChild(iframe);

    currentDocumentFrame = iframe;

    modal.style.display = "block";
    document.body.style.overflow = "hidden";
}


function closeDocumentViewer() {

    const modal = document.getElementById("documentViewerModal");

    if (currentDocumentFrame) {
        currentDocumentFrame.src = "about:blank";
        currentDocumentFrame.remove();
        currentDocumentFrame = null;
    }

    const body = document.querySelector(".document-body");

    if (body) {
        body.innerHTML = "";
    }

    modal.style.display = "none";
    document.body.style.overflow = "";
}
// ============================================
// EVENT LISTENERS
// ============================================

// Close application modal when clicking outside
window.addEventListener("click", function(event) {
    const modal = document.getElementById("applicationModal");
    if (event.target === modal) {
        closeApplicationView();
    }

    // Close document viewer when clicking outside
    const viewerModal = document.getElementById("documentViewerModal");
    if (event.target === viewerModal) {
        closeDocumentViewer();
    }
});

// Close modals with Escape key
document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        const viewerModal = document.getElementById("documentViewerModal");
        if (viewerModal && viewerModal.style.display === "block") {
            closeDocumentViewer();
        }

        const appModal = document.getElementById("applicationModal");
        if (appModal && appModal.style.display === "block") {
            closeApplicationView();
        }
    }
});