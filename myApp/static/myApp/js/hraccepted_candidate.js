// ============================================================
// HR ACCEPTED CANDIDATES – JavaScript
// ============================================================

console.log("HR Accepted Candidates JS Loaded");

// ============================================================
// APPLICATION VIEW MODAL
// ============================================================

function openApplicationView(applicationId, source) {

    console.log("Opening application:", applicationId);

    const modal = document.getElementById("applicationModal");
    const applicationContent = document.getElementById("applicationContent");

    if (!modal || !applicationContent) {
        console.error("Modal elements missing");
        return;
    }

    modal.style.display = "block";
    document.body.style.overflow = "hidden";

    applicationContent.innerHTML = `
        <div class="loading-profile">
            <i class="fas fa-spinner fa-spin"></i>
            Loading application...
        </div>
    `;

    let url = `/hrapplication-view/${applicationId}/`;

    if (source) {
        url += `?source=${source}`;
    } else {
        url += `?source=hraccepted`;
    }

    fetch(url)
        .then(response => {

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            return response.text();

        })
        .then(html => {

            applicationContent.innerHTML = html;

        })
        .catch(error => {

            console.error(error);

            applicationContent.innerHTML = `
                <div class="error-profile">
                    <i class="fas fa-exclamation-circle"></i>
                    Failed to load application.
                </div>
            `;

        });

}

function closeApplicationView() {

    const modal = document.getElementById("applicationModal");
    const applicationContent = document.getElementById("applicationContent");

    if (modal) {

        modal.style.display = "none";
        document.body.style.overflow = "";

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

// ============================================================
// DOCUMENT VIEWER
// ============================================================

function openDocumentViewer(documentUrl, documentName) {

    console.log("Opening:", documentName);

    const modal = document.getElementById("documentViewerModal");
    const body = document.querySelector(".document-body");
    const title = document.getElementById("documentTitle");

    if (!modal || !body || !title) {

        console.error("Document viewer elements missing");
        return;

    }

    title.textContent = documentName || "Document Viewer";

    // Completely destroy previous viewer
    body.innerHTML = "";

    // Create a fresh iframe every time
    const iframe = document.createElement("iframe");

    iframe.id = "documentFrame";
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.border = "none";

    // Force browser to reload PDF
    const fullUrl = documentUrl.startsWith("http")
        ? documentUrl
        : window.location.origin + documentUrl;

    iframe.src =
        fullUrl +
        (fullUrl.includes("?") ? "&" : "?") +
        "_=" +
        new Date().getTime();

    body.appendChild(iframe);

    modal.style.display = "block";
    document.body.style.overflow = "hidden";

}

function closeDocumentViewer() {

    const modal = document.getElementById("documentViewerModal");
    const body = document.querySelector(".document-body");

    if (modal) {
        modal.style.display = "none";
    }

    // Destroy iframe completely
    if (body) {
        body.innerHTML = "";
    }

    document.body.style.overflow = "";

}

// ============================================================
// SCHEDULE INTERVIEW
// ============================================================

function scheduleInterview(applicationId) {

    console.log("Schedule interview:", applicationId);

    alert(
        `Interview scheduling functionality will be implemented for application ${applicationId}`
    );

}

// ============================================================
// CLOSE MODALS WHEN CLICKING OUTSIDE
// ============================================================

window.addEventListener("click", function(event) {

    const applicationModal = document.getElementById("applicationModal");

    if (applicationModal && event.target === applicationModal) {
        closeApplicationView();
    }

    const documentModal = document.getElementById("documentViewerModal");

    if (documentModal && event.target === documentModal) {
        closeDocumentViewer();
    }

});

// ============================================================
// DOM READY
// ============================================================

document.addEventListener("DOMContentLoaded", function() {

    // Escape key

    document.addEventListener("keydown", function(event) {

        if (event.key !== "Escape") return;

        const applicationModal = document.getElementById("applicationModal");

        if (applicationModal &&
            applicationModal.style.display === "block") {

            closeApplicationView();

        }

        const documentModal = document.getElementById("documentViewerModal");

        if (documentModal &&
            documentModal.style.display === "block") {

            closeDocumentViewer();

        }

    });

    // Hover animation

    document.querySelectorAll(".view-application-btn").forEach(button => {

        button.addEventListener("mouseenter", function() {

            this.style.transform = "translateY(-1px)";

        });

        button.addEventListener("mouseleave", function() {

            this.style.transform = "translateY(0)";

        });

    });

    // Send to Admin confirmation

    document.querySelectorAll(".btn-send-admin").forEach(button => {

        button.addEventListener("click", function(e) {

            if (
                !confirm(
                    "Are you sure you want to send this candidate to Admin for final approval?"
                )
            ) {

                e.preventDefault();

            }

        });

    });

});

// ============================================================
// GLOBAL FUNCTIONS
// ============================================================

window.openApplicationView = openApplicationView;
window.closeApplicationView = closeApplicationView;
window.openDocumentViewer = openDocumentViewer;
window.closeDocumentViewer = closeDocumentViewer;
window.scheduleInterview = scheduleInterview;