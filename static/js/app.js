/**
 * HTASO Umpire Evaluation - Client-side JavaScript
 * Handles form interactions, validation, and UI enhancements
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Initialize DataTables if table exists
    const evalTable = document.getElementById('evaluationsTable');
    if (evalTable && typeof $ !== 'undefined' && $.fn.DataTable) {
        $(evalTable).DataTable({
            order: [[3, 'desc']], // Sort by submission date descending
            pageLength: 25,
            language: {
                search: "Search evaluations:",
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ evaluations"
            }
        });
    }

    // Form submission loading state
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]:focus, button[type="submit"]:hover');
            if (submitBtn && !submitBtn.formNoValidate) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            }
        });
    });

    // Password match validation
    const confirmPassword = document.getElementById('confirm_password');
    const newPassword = document.getElementById('new_password');
    if (confirmPassword && newPassword) {
        confirmPassword.addEventListener('input', function() {
            if (this.value !== newPassword.value) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });

        newPassword.addEventListener('input', function() {
            if (confirmPassword.value && confirmPassword.value !== this.value) {
                confirmPassword.setCustomValidity('Passwords do not match');
            } else {
                confirmPassword.setCustomValidity('');
            }
        });
    }

    // Date input enhancements (simple MM/DD/YYYY format helper)
    const dateInputs = document.querySelectorAll('input[type="text"][placeholder*="MM/DD/YYYY"]');
    dateInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
            if (value.length >= 2) {
                value = value.substring(0, 2) + '/' + value.substring(2);
            }
            if (value.length >= 5) {
                value = value.substring(0, 5) + '/' + value.substring(5, 9);
            }
            e.target.value = value.substring(0, 10);
        });

        input.addEventListener('blur', function(e) {
            const value = e.target.value;
            if (value && value.length === 10) {
                // Basic validation
                const parts = value.split('/');
                const month = parseInt(parts[0]);
                const day = parseInt(parts[1]);
                const year = parseInt(parts[2]);

                if (month < 1 || month > 12 || day < 1 || day > 31 || year < 1900) {
                    alert('Please enter a valid date in MM/DD/YYYY format');
                    e.target.value = '';
                }
            }
        });
    });

    // Recommendation radio button visual feedback
    const recommendationRadios = document.querySelectorAll('input[name="recommendation"]');
    recommendationRadios.forEach(function(radio) {
        radio.addEventListener('change', function() {
            // Update all indicators
            document.querySelectorAll('.recommendation-indicator').forEach(function(indicator) {
                indicator.style.backgroundColor = '#D1D5DB'; // Reset to border color
            });

            // Highlight selected
            const selectedOption = this.closest('.recommendation-option');
            if (selectedOption) {
                const indicator = selectedOption.querySelector('.recommendation-indicator');
                const currentColor = indicator.style.backgroundColor;
                // Keep the original color (it's set in inline style from template)
            }
        });
    });

    // Smooth scroll to first error on form submission
    const firstError = document.querySelector('.is-invalid');
    if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstError.focus();
    }

    // Confirm before leaving page with unsaved changes
    let formChanged = false;
    const mainForm = document.getElementById('evaluationForm');
    if (mainForm) {
        mainForm.addEventListener('change', function() {
            formChanged = true;
        });

        window.addEventListener('beforeunload', function(e) {
            if (formChanged) {
                e.preventDefault();
                e.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
                return e.returnValue;
            }
        });

        mainForm.addEventListener('submit', function() {
            formChanged = false; // Allow navigation after submit
        });
    }

    // Tooltip initialization (if Bootstrap tooltips are used)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Export button loading states
    const exportButtons = document.querySelectorAll('button[formaction*="export"]');
    exportButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            const originalText = this.innerHTML;
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';

            // Re-enable after 3 seconds (file download should start by then)
            setTimeout(function() {
                btn.disabled = false;
                btn.innerHTML = originalText;
            }, 3000);
        });
    });

    // Real-time section score calculation
    const ratingSelects = document.querySelectorAll('.rating-select');
    console.log('Found ' + ratingSelects.length + ' rating selects');

    ratingSelects.forEach(function(select) {
        select.addEventListener('change', function() {
            console.log('Rating changed:', this.value);
            updateSectionScores();
        });
    });

    // Initialize section scores on page load
    setTimeout(function() {
        updateSectionScores();
    }, 100);
});

/**
 * Update all section scores based on current ratings
 */
function updateSectionScores() {
    const scoreBadges = document.querySelectorAll('.section-score-badge');
    console.log('Found ' + scoreBadges.length + ' score badges');

    scoreBadges.forEach(function(badge) {
        const section = badge.dataset.section;
        const subsection = badge.dataset.subsection;

        // Find all rating selects for this subsection
        const selects = document.querySelectorAll(
            `.rating-select[data-section="${section}"][data-subsection="${subsection}"]`
        );

        console.log(`Section: ${subsection}, Found ${selects.length} selects`);

        let totalScore = 0;
        let htasoTotal = 0;
        let maxPossible = 0;
        let ratedCount = 0;

        selects.forEach(function(select) {
            const value = select.value;
            console.log(`  Select value: ${value}`);

            // Skip if not rated or "Select result"
            if (!value || value === 'Select result' || value === 'Not Observed') {
                return;
            }

            // Extract numeric value and invert (HTASO: 1=best, 5=worst -> internal: 5=best, 1=worst)
            const match = value.match(/^(\d+)/);
            if (match) {
                const htasoScore = parseInt(match[1]);
                const score = 6 - htasoScore;
                totalScore += score;
                htasoTotal += htasoScore;
                maxPossible += 5; // Maximum is always 5
                ratedCount++;
                console.log(`    Counted: HTASO ${htasoScore}, internal ${score} points`);
            }
        });

        console.log(`  Total: ${totalScore}/${maxPossible} (${ratedCount} rated)`);

        // Update badge display
        const scoreAvg = badge.querySelector('.score-avg');
        const scoreRank = badge.querySelector('.score-rank');
        const scorePercentage = badge.querySelector('.score-percentage');

        if (ratedCount === 0) {
            if (scoreAvg) scoreAvg.textContent = '\u2014';
            if (scoreRank) scoreRank.textContent = '\u2014';
            scorePercentage.textContent = '0%';
            badge.classList.remove('bg-success', 'bg-warning', 'bg-danger');
            badge.classList.add('bg-info');
        } else {
            const htasoAvg = htasoTotal / ratedCount;
            const rank = Math.round(htasoAvg);
            const percentage = Math.round((totalScore / maxPossible) * 100);

            if (scoreAvg) scoreAvg.textContent = htasoAvg.toFixed(2);
            if (scoreRank) scoreRank.textContent = rank;
            scorePercentage.textContent = `${percentage}%`;

            // Color code based on HTASO rank (1=best, 5=worst)
            badge.classList.remove('bg-info', 'bg-success', 'bg-warning', 'bg-danger');
            if (rank <= 2) {
                badge.classList.add('bg-success');
            } else if (rank <= 3) {
                badge.classList.add('bg-warning');
            } else {
                badge.classList.add('bg-danger');
            }
        }
    });
}

/**
 * Show a toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type of toast (success, error, info, warning)
 */
function showToast(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    const container = document.querySelector('.container-fluid') || document.body;
    container.insertBefore(alertDiv, container.firstChild);

    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

/**
 * Validate evaluation form before submission
 * @returns {boolean} - True if form is valid
 */
function validateEvaluationForm() {
    const evaluatorName = document.getElementById('evaluator_name');
    const trainerName = document.getElementById('trainer_name');
    const trainingDate = document.getElementById('training_date');
    const recommendation = document.querySelector('input[name="recommendation"]:checked');

    let isValid = true;
    const errors = [];

    if (!evaluatorName || !evaluatorName.value.trim()) {
        errors.push('Evaluator Name is required');
        isValid = false;
    }

    if (!trainerName || !trainerName.value.trim()) {
        errors.push('Trainer Name is required');
        isValid = false;
    }

    if (!trainingDate || !trainingDate.value.trim()) {
        errors.push('Training Date is required');
        isValid = false;
    }

    if (!recommendation) {
        errors.push('Overall Recommendation is required');
        isValid = false;
    }

    if (!isValid) {
        showToast(errors.join('<br>'), 'error');
    }

    return isValid;
}
