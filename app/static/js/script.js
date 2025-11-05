document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const incidentForm = document.getElementById('incidentForm');
    if (incidentForm) {
        incidentForm.addEventListener('submit', function(e) {
            const description = document.getElementById('description').value;
            if (description.trim().length < 10) {
                e.preventDefault();
                alert('Please provide a more detailed incident description (at least 10 characters).');
                return false;
            }
        });
    }

    // Dynamic risk indicator
    const severitySelect = document.getElementById('severity');
    if (severitySelect) {
        severitySelect.addEventListener('change', updateRiskIndicator);
    }

    function updateRiskIndicator() {
        const severity = severitySelect.value;
        const riskIndicator = document.getElementById('riskIndicator');
        if (riskIndicator) {
            riskIndicator.textContent = `Selected Severity: ${severity.toUpperCase()}`;
            riskIndicator.className = `risk-${severity}`;
        }
    }

    // Auto-save form data
    const formFields = ['description', 'incident_type', 'severity', 'jurisdiction'];
    
    formFields.forEach(field => {
        const element = document.getElementById(field);
        if (element) {
            // Load saved data
            const saved = localStorage.getItem(`incident_${field}`);
            if (saved) {
                element.value = saved;
            }
            
            // Save on input
            element.addEventListener('input', function() {
                localStorage.setItem(`incident_${field}`, this.value);
            });
        }
    });

    // Confidence meter animation
    const confidenceMeter = document.querySelector('.confidence-fill');
    if (confidenceMeter) {
        const confidence = parseFloat(confidenceMeter.parentElement.dataset.confidence);
        setTimeout(() => {
            confidenceMeter.style.width = `${confidence * 100}%`;
        }, 500);
    }

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                setTimeout(() => {
                    this.textContent = originalText;
                }, 2000);
            });
        });
    });
});

// API integration for real-time analysis
async function analyzeText(text) {
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ description: text })
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Analysis error:', error);
        return null;
    }
}
