// ============================================================
// HR APPLICANTS – JavaScript (hrapplicants.js)
// Handles modal interactions, profile fetching, and UI updates.
// Data logic remains untouched.
// ============================================================

console.log("HR Applicants JS Loaded");

/**
 * Opens the applicant profile modal and fetches profile data
 * @param {string|number} userId - The ID of the applicant
 */
function openApplicantProfile(userId) {
    // Get modal elements
    const modal = document.getElementById("applicantProfileModal");
    const profileContent = document.getElementById("profileContent");

    // Show modal
    modal.style.display = "block";

    // Show loading state
    profileContent.innerHTML = `
        <div class="loading-profile">
            <i class="fas fa-spinner fa-spin"></i>
            Loading profile...
        </div>
    `;

    // Fetch profile data via AJAX
    fetch(`/hrapplicant-profile/${userId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            profileContent.innerHTML = html;
        })
        .catch(error => {
            console.error("Error loading profile:", error);
            profileContent.innerHTML = `
                <div class="error-profile">
                    <i class="fas fa-exclamation-circle"></i>
                    Failed to load profile. Please try again.
                </div>
            `;
        });
}

/**
 * Closes the applicant profile modal
 */
function closeApplicantProfile() {
    const modal = document.getElementById("applicantProfileModal");
    modal.style.display = "none";
}

// ============================================================
// CLOSE MODAL ON OUTSIDE CLICK
// ============================================================
document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("applicantProfileModal");

    // Close modal when clicking outside the content
    modal.addEventListener("click", function(event) {
        if (event.target === modal) {
            closeApplicantProfile();
        }
    });

    // Close modal with Escape key
    document.addEventListener("keydown", function(event) {
        if (event.key === "Escape" && modal.style.display === "block") {
            closeApplicantProfile();
        }
    });
});

// ============================================================
// (Optional) Handle any dynamic table interactions
// ============================================================
document.addEventListener("DOMContentLoaded", function() {
    // Add hover effects or additional interactivity if needed
    const viewButtons = document.querySelectorAll(".view-profile-btn");
    viewButtons.forEach(button => {
        button.addEventListener("mouseenter", function() {
            this.style.transform = "translateY(-1px)";
        });
        button.addEventListener("mouseleave", function() {
            this.style.transform = "translateY(0)";
        });
    });
});