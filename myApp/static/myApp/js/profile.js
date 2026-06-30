// ============================================================
// PROFILE PAGE JAVASCRIPT
// Complete Profile Management System
// ============================================================

// ============================================================
// SECTION 1: MODAL MANAGEMENT
// ============================================================

/**
 * Open a modal by ID
 * @param {string} id - The ID of the modal to open
 */
function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = "flex";
        document.body.style.overflow = "hidden";
    }
}

/**
 * Close a modal by ID
 * @param {string} id - The ID of the modal to close
 */
function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = "none";
        document.body.style.overflow = "";
    }
}

/**
 * Close modal when clicking outside
 */
window.addEventListener("click", function(event) {
    document.querySelectorAll(".modal").forEach(modal => {
        if (event.target === modal) {
            modal.style.display = "none";
            document.body.style.overflow = "";
        }
    });
});

/**
 * Close modal with Escape key
 */
document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        document.querySelectorAll(".modal").forEach(modal => {
            modal.style.display = "none";
            document.body.style.overflow = "";
        });
    }
});

// ============================================================
// SECTION 2: MOBILE MENU
// ============================================================

/**
 * Toggle mobile menu visibility
 */
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const toggleBtn = document.querySelector('.mobile-menu-toggle');
    
    if (navMenu) {
        navMenu.classList.toggle('open');
        
        if (toggleBtn) {
            const icon = toggleBtn.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-times');
            }
        }
    }
}

/**
 * Close mobile menu on link click (mobile only)
 */
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-links a');
    const navMenu = document.querySelector('.nav-menu');
    const toggleBtn = document.querySelector('.mobile-menu-toggle');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 968) {
                navMenu.classList.remove('open');
                if (toggleBtn) {
                    const icon = toggleBtn.querySelector('i');
                    if (icon) {
                        icon.classList.remove('fa-times');
                        icon.classList.add('fa-bars');
                    }
                }
            }
        });
    });
});

// ============================================================
// SECTION 3: USER MENU DROPDOWN
// ============================================================

/**
 * Toggle user dropdown menu
 */
function toggleUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    const circle = document.querySelector('.user-circle');
    
    if (dropdown) {
        dropdown.classList.toggle('show');
        const expanded = dropdown.classList.contains('show');
        if (circle) {
            circle.setAttribute('aria-expanded', expanded);
        }
    }
}

/**
 * Close user dropdown when clicking outside
 */
document.addEventListener('click', function(event) {
    const userMenu = document.querySelector('.user-menu');
    const dropdown = document.getElementById('userDropdown');
    
    if (userMenu && dropdown) {
        if (!userMenu.contains(event.target)) {
            dropdown.classList.remove('show');
            const circle = document.querySelector('.user-circle');
            if (circle) {
                circle.setAttribute('aria-expanded', 'false');
            }
        }
    }
});

// ============================================================
// SECTION 4: DASHBOARD TOGGLE
// ============================================================

/**
 * Toggle dashboard section visibility
 * @param {string} contentId - The ID of the content to toggle
 */
function toggleSection(contentId) {
    const content = document.getElementById(contentId);
    const header = content ? content.closest('.dashboard-container').querySelector('.dashboard-header') : null;
    
    if (content && header) {
        if (content.style.display === 'none' || content.style.display === '') {
            content.style.display = 'block';
            header.classList.add('active');
        } else {
            content.style.display = 'none';
            header.classList.remove('active');
        }
    }
}

// ============================================================
// SECTION 5: WORK EXPERIENCE
// ============================================================

/**
 * Toggle work experience fields visibility
 */
function toggleWorkFields() {
    const experienceSelect = document.getElementById("hasExperience");
    const workFields = document.getElementById("workFields");

    if (!experienceSelect || !workFields) {
        return;
    }

    if (experienceSelect.value === "yes") {
        workFields.style.display = "block";
    } else {
        workFields.style.display = "none";
    }
}

/**
 * Toggle end date field based on currently working checkbox
 */
function toggleEndDate() {
    const currentlyWorking = document.getElementById("currentlyWorking");
    const endDateContainer = document.getElementById("endDateContainer");
    const endDate = document.getElementById("endDate");

    if (!currentlyWorking || !endDateContainer || !endDate) {
        return;
    }

    if (currentlyWorking.checked) {
        endDate.value = "";
        endDate.disabled = true;
        endDateContainer.style.opacity = "0.5";
    } else {
        endDate.disabled = false;
        endDateContainer.style.opacity = "1";
    }
}

/**
 * Open modal to add new work experience
 */
function openAddWorkModal() {
    // Reset form fields
    document.getElementById("workModalTitle").innerText = "Add Work Experience";
    document.getElementById("work_id").value = "";
    document.getElementById("hasExperience").value = "yes";
    document.getElementById("workFields").style.display = "block";
    
    document.querySelector('[name="company"]').value = "";
    document.querySelector('[name="job_title"]').value = "";
    document.querySelector('[name="description"]').value = "";
    document.querySelector('[name="start_date"]').value = "";
    document.querySelector('[name="end_date"]').value = "";
    document.querySelector('[name="reason_for_leaving"]').value = "";
    
    const checkbox = document.getElementById("currentlyWorking");
    if (checkbox) {
        checkbox.checked = false;
    }
    toggleEndDate();
    
    openModal("workModal");
}

/**
 * Open modal to edit existing work experience
 */
function openEditWorkModal(id, company, jobTitle, description, startDate, endDate, reason, currentlyWorking) {
    openModal("workModal");

    document.getElementById("workModalTitle").innerText = "Edit Work Experience";
    document.getElementById("work_id").value = id;
    document.getElementById("hasExperience").value = "yes";
    document.getElementById("workFields").style.display = "block";

    document.querySelector('[name="company"]').value = company || "";
    document.querySelector('[name="job_title"]').value = jobTitle || "";
    document.querySelector('[name="description"]').value = description || "";
    document.querySelector('[name="start_date"]').value = startDate || "";
    document.querySelector('[name="end_date"]').value = endDate || "";
    document.querySelector('[name="reason_for_leaving"]').value = reason || "";

    const checkbox = document.getElementById("currentlyWorking");
    if (checkbox) {
        checkbox.checked = currentlyWorking === "true";
    }
    toggleEndDate();
}

/**
 * Toggle view more/less for work experience
 */
function toggleWorkExperience() {
    const extraWork = document.querySelectorAll(".extra-work");
    const button = document.getElementById("workMoreBtn");

    if (!extraWork.length || !button) return;

    const isExpanded = button.innerText === "Show Less";

    extraWork.forEach(card => {
        card.style.display = isExpanded ? "none" : "block";
    });

    button.innerText = isExpanded ? "View More" : "Show Less";
    button.innerHTML = isExpanded 
        ? '<i class="fas fa-chevron-down"></i> View More' 
        : '<i class="fas fa-chevron-up"></i> Show Less';
}

// ============================================================
// SECTION 6: EDUCATION
// ============================================================

/**
 * Open modal to add new education record
 */
function openAddEducationModal() {
    document.getElementById("education_id").value = "";
    document.getElementById("school_name").value = "";
    document.getElementById("qualification").value = "";
    document.getElementById("qualification_level").value = "";
    document.getElementById("education_start_date").value = "";
    document.getElementById("education_end_date").value = "";
    document.getElementById("educationModalTitle").innerText = "Add Education";
    
    openModal("educationModal");
}

/**
 * Open modal to edit existing education record
 */
function openEditEducationModal(id, school, qualification, qualificationLevel, startDate, endDate) {
    document.getElementById("education_id").value = id;
    document.getElementById("school_name").value = school || "";
    document.getElementById("qualification").value = qualification || "";
    document.getElementById("qualification_level").value = qualificationLevel || "";
    document.getElementById("education_start_date").value = startDate || "";
    document.getElementById("education_end_date").value = endDate || "";
    document.getElementById("educationModalTitle").innerText = "Edit Education";
    
    openModal("educationModal");
}

/**
 * Show all education cards
 */
function showMoreEducation() {
    const cards = document.querySelectorAll(".education-card");
    const button = document.getElementById("educationMoreBtn");

    cards.forEach(card => {
        card.style.display = "block";
    });

    if (button) {
        button.style.display = "none";
    }
}

// ============================================================
// SECTION 7: QUALIFICATION CERTIFICATES
// ============================================================

/**
 * Open modal to edit qualification
 */
function openEditQualificationModal(id, name, certificate) {
    document.getElementById("qualification_id").value = id;
    document.getElementById("qualification_name").value = name || "";
    
    // Reset remove action
    document.getElementById("remove_certificate").value = "false";
    
    // Clear selected file
    document.getElementById("certificateInput").value = "";
    
    // Reset button text
    document.getElementById("certificateLabel").innerText = "Replace Certificate";
    
    const certificateDisplay = document.getElementById("current_certificate");
    
    if (certificate) {
        certificateDisplay.innerText = certificate;
    } else {
        certificateDisplay.innerText = "No certificate uploaded.";
    }
    
    openModal("editQualificationModal");
}

/**
 * Remove qualification certificate (mark for deletion)
 */
function removeQualificationCertificate() {
    document.getElementById("remove_certificate").value = "true";
    document.getElementById("current_certificate").innerHTML = "Certificate will be removed unless replaced.";
    document.getElementById("certificateInput").value = "";
    document.getElementById("certificateLabel").innerText = "Choose Replacement Certificate";
}

/**
 * Toggle view more/less for qualifications
 */
function toggleQualifications() {
    const cards = document.querySelectorAll(".qualification-item");
    const button = document.getElementById("qualificationMoreBtn");

    if (!cards.length || !button) return;

    const isExpanded = button.innerText.includes("Show Less");

    cards.forEach((card, index) => {
        if (index > 0) {
            card.style.display = isExpanded ? "none" : "block";
        }
    });

    button.innerHTML = isExpanded
        ? '<i class="fas fa-chevron-down"></i> View More'
        : '<i class="fas fa-chevron-up"></i> Show Less';
}

/**
 * Update certificate label when file is selected
 */
function updateCertificateLabel() {
    const input = document.getElementById("certificateInput");
    const label = document.getElementById("certificateLabel");

    if (input && input.files.length > 0) {
        label.innerText = input.files[0].name;
        
        // Cancel delete request if replacing certificate
        document.getElementById("remove_certificate").value = "false";
        document.getElementById("current_certificate").innerHTML = "Replacing with: " + input.files[0].name;
    }
}

// ============================================================
// SECTION 8: DOCUMENT MANAGEMENT
// ============================================================

let selectedDocument = "";

/**
 * Open document modal
 */
function openDocumentModal(type, filename) {
    selectedDocument = type;
    document.getElementById("current_document").innerText = filename;
    openModal("documentsModal");
}

/**
 * Remove current document (mark for deletion)
 */
function removeCurrentDocument() {
    if (selectedDocument === "resume") {
        document.getElementById("remove_resume").value = "true";
    }
    
    if (selectedDocument === "id_document") {
        document.getElementById("remove_id_document").value = "true";
    }
    
    if (selectedDocument === "matric_certificate") {
        document.getElementById("remove_matric_certificate").value = "true";
    }
    
    document.getElementById("current_document").innerText = "Document will be removed.";
}

/**
 * Remove resume
 */
function removeResume() {
    document.getElementById("remove_resume").value = "true";
    document.getElementById("resume_display").innerHTML = "Resume will be removed unless replaced.";
    document.getElementById("resumeInput").value = "";
    document.getElementById("resumeLabel").innerText = "Choose Replacement File";
}

/**
 * Remove ID document
 */
function removeIDDocument() {
    document.getElementById("remove_id_document").value = "true";
    document.getElementById("id_document_display").innerHTML = "ID Document will be removed unless replaced.";
    document.getElementById("idDocumentInput").value = "";
    document.getElementById("idDocumentLabel").innerText = "Choose Replacement File";
}

/**
 * Remove matric certificate
 */
function removeMatricCertificate() {
    document.getElementById("remove_matric_certificate").value = "true";
    document.getElementById("matric_display").innerHTML = "Matric Certificate will be removed unless replaced.";
    document.getElementById("matricInput").value = "";
    document.getElementById("matricLabel").innerText = "Choose Replacement File";
}

/**
 * Update file label when file is selected
 */
function updateFileLabel(inputId, labelId) {
    const input = document.getElementById(inputId);
    const label = document.getElementById(labelId);

    if (input && input.files.length > 0) {
        label.innerText = input.files[0].name;

        // Cancel delete request if user chooses a replacement
        if (inputId === "resumeInput") {
            document.getElementById("remove_resume").value = "false";
            document.getElementById("resume_display").innerHTML = "Replacing with: " + input.files[0].name;
        }

        if (inputId === "idDocumentInput") {
            document.getElementById("remove_id_document").value = "false";
            document.getElementById("id_document_display").innerHTML = "Replacing with: " + input.files[0].name;
        }

        if (inputId === "matricInput") {
            document.getElementById("remove_matric_certificate").value = "false";
            document.getElementById("matric_display").innerHTML = "Replacing with: " + input.files[0].name;
        }
    }
}

// ============================================================
// SECTION 9: URL TRUNCATION
// ============================================================

/**
 * Truncate long URLs in the profile (fallback for Django's truncatechars)
 */
document.addEventListener('DOMContentLoaded', function() {
    const urlElements = document.querySelectorAll('.url-truncate .truncate-link');
    
    urlElements.forEach(element => {
        // Get the full text content
        let fullText = element.textContent.trim();
        // Remove the icon text if present
        fullText = fullText.replace(/[^\w\s\/:.-]/g, '').trim();
        
        // If the text is longer than 35 characters, truncate it
        if (fullText.length > 35) {
            const truncated = fullText.substring(0, 32) + '...';
            // Keep the icon if present
            const icon = element.querySelector('i');
            if (icon) {
                element.innerHTML = '';
                element.appendChild(icon);
                element.appendChild(document.createTextNode(' ' + truncated));
            } else {
                element.textContent = truncated;
            }
            // Set title for tooltip
            element.title = fullText;
        }
    });
});

// ============================================================
// SECTION 10: INITIALIZATION
// ============================================================

/**
 * Initialize dashboard sections
 */
document.addEventListener('DOMContentLoaded', function() {
    // "Your Details" section starts open
    const detailsContent = document.getElementById('detailsContent');
    const detailsHeader = document.querySelector('.dashboard-container .dashboard-header');
    
    if (detailsContent) {
        detailsContent.style.display = 'block';
        if (detailsHeader) {
            detailsHeader.classList.add('active');
        }
    }
    
    // "Your Applications" section starts closed
    const applicationsContent = document.getElementById('applicationsContent');
    const applicationsHeader = document.querySelector('.dashboard-container:last-child .dashboard-header');
    
    if (applicationsContent) {
        applicationsContent.style.display = 'none';
        if (applicationsHeader) {
            applicationsHeader.classList.remove('active');
        }
    }
    
    // Initialize work experience fields if they exist
    const hasExperience = document.getElementById('hasExperience');
    if (hasExperience && hasExperience.value === 'yes') {
        const workFields = document.getElementById('workFields');
        if (workFields) {
            workFields.style.display = 'block';
        }
    }
    
    // Initialize end date state
    const currentlyWorking = document.getElementById('currentlyWorking');
    if (currentlyWorking && currentlyWorking.checked) {
        toggleEndDate();
    }
    
    // Handle truncation for URLs with truncatechars fallback
    truncateUrlLinks();
});

/**
 * Truncate URL links (fallback if Django truncatechars doesn't work)
 */
function truncateUrlLinks() {
    const links = document.querySelectorAll('.url-truncate .truncate-link');
    
    links.forEach(link => {
        // Get the text content excluding the icon
        const icon = link.querySelector('i');
        let text = link.textContent.trim();
        
        // If there's an icon, remove it from the text
        if (icon) {
            text = text.replace(icon.textContent, '').trim();
        }
        
        // If text is longer than 35 chars, truncate
        if (text.length > 35) {
            const truncated = text.substring(0, 32) + '...';
            if (icon) {
                // Clear and rebuild with icon + truncated text
                link.innerHTML = '';
                link.appendChild(icon);
                link.appendChild(document.createTextNode(' ' + truncated));
            } else {
                link.textContent = truncated;
            }
            // Set title attribute for tooltip on hover
            link.title = text;
        }
    });
}

/**
 * Handle window resize for responsive behavior
 */
window.addEventListener('resize', function() {
    // Reset mobile menu on resize to desktop
    if (window.innerWidth > 968) {
        const navMenu = document.querySelector('.nav-menu');
        const toggleBtn = document.querySelector('.mobile-menu-toggle');
        
        if (navMenu) {
            navMenu.classList.remove('open');
        }
        
        if (toggleBtn) {
            const icon = toggleBtn.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    }
});

// ============================================================
// SECTION 11: FORM VALIDATION HELPERS
// ============================================================

/**
 * Show field error message
 * @param {HTMLElement} field - The field element
 * @param {string} message - Error message to display
 */
function showFieldError(field, message) {
    // Highlight field
    field.classList.add('error');
    field.style.borderColor = '#dc2626';
    field.style.boxShadow = '0 0 0 4px rgba(220, 38, 38, 0.1)';
    
    // Create error message if not exists
    let errorEl = field.parentElement.querySelector('.field-error');
    if (!errorEl) {
        errorEl = document.createElement('span');
        errorEl.className = 'field-error';
        errorEl.style.cssText = `
            color: #dc2626;
            font-size: 0.8rem;
            margin-top: 0.25rem;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        `;
        field.parentElement.appendChild(errorEl);
    }
    errorEl.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    
    // Remove error on focus
    field.addEventListener('focus', function() {
        this.classList.remove('error');
        this.style.borderColor = '';
        this.style.boxShadow = '';
        const err = this.parentElement.querySelector('.field-error');
        if (err) err.remove();
    }, { once: true });
}

// ============================================================
// SECTION 12: AUTO-DISMISS MESSAGES
// ============================================================

/**
 * Auto-dismiss messages after 5 seconds
 */
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');
    
    messages.forEach((message, index) => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        }, 5000 + (index * 500));
    });
});

// ============================================================
// SECTION 13: DOCUMENT VIEWER
// ============================================================

function openDocumentViewer(url, title) {
    const modal = document.getElementById("documentViewerModal");
    const frame = document.getElementById("documentFrame");
    const titleElement = document.getElementById("documentTitle");

    if (!modal || !frame) {
        console.error("Document viewer not found");
        return;
    }

    titleElement.innerText = title;
    frame.data = url;
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
}

function closeDocumentViewer() {
    const modal = document.getElementById("documentViewerModal");
    const frame = document.getElementById("documentFrame");

    if (modal) {
        modal.style.display = "none";
    }

    if (frame) {
        frame.data = "";
    }

    document.body.style.overflow = "";
}

// ============================================================
// SECTION 14: PROFILE ALERT
// ============================================================

document.addEventListener("DOMContentLoaded", function() {
    const warning = document.getElementById("profileWarning");

    if (!warning) return;

    warning.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
});

// ============================================================
// SECTION 15: PROFILE SECTION SCROLL
// ============================================================

document.addEventListener("DOMContentLoaded", function() {
    const profileData = document.getElementById("profile-data");

    if (!profileData) {
        return;
    }

    const section = profileData.dataset.section;
    let target = null;

    if (section === "personal") {
        target = document.getElementById("personalSection");
    } else if (section === "contact") {
        target = document.getElementById("contactSection");
    } else if (section === "documents") {
        target = document.getElementById("documentsSection");
    }

    if (target) {
        setTimeout(function() {
            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }, 300);
    }
});

// ============================================================
// SECTION 16: TOGGLE APPLICATIONS
// ============================================================

/**
 * Toggle view more/less for applications
 */
function toggleApplications() {
    const extraApps = document.querySelectorAll(".extra-application");
    const button = document.getElementById("applicationMoreBtn");

    if (!extraApps.length || !button) return;

    const isExpanded = button.innerText.includes("Show Less");

    extraApps.forEach(card => {
        card.style.display = isExpanded ? "none" : "block";
    });

    button.innerHTML = isExpanded
        ? '<i class="fas fa-chevron-down"></i> View More'
        : '<i class="fas fa-chevron-up"></i> Show Less';
}