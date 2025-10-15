// Configuration
const REPORTS_BASE_URL = 'reports/';
let currentReport = 'bob-weekly';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadReport(currentReport);
    setupNavigation();
    loadLastUpdated();
});

// Setup navigation
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const reportName = btn.dataset.report;
            switchReport(reportName, btn);
        });
    });
}

// Switch to a different report
function switchReport(reportName, button) {
    // Update active button
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    button.classList.add('active');

    // Load new report
    currentReport = reportName;
    loadReport(reportName);
}

// Load and display report
async function loadReport(reportName) {
    const loadingEl = document.getElementById('loading');
    const contentEl = document.getElementById('report-content');
    const shareEl = document.getElementById('share-section');

    // Show loading
    loadingEl.style.display = 'block';
    contentEl.style.display = 'none';
    shareEl.style.display = 'none';

    try {
        // Fetch markdown file
        const response = await fetch(`${REPORTS_BASE_URL}${reportName}.md`);
        if (!response.ok) {
            throw new Error(`Failed to load report: ${response.status}`);
        }

        const markdown = await response.text();

        // Convert markdown to HTML
        const html = marked.parse(markdown);

        // Display content
        contentEl.innerHTML = html;
        contentEl.style.display = 'block';
        shareEl.style.display = 'block';
        loadingEl.style.display = 'none';

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });

    } catch (error) {
        console.error('Error loading report:', error);
        contentEl.innerHTML = `
            <div style="text-align: center; padding: 2rem;">
                <h2>⚠️ Error Loading Report</h2>
                <p>Could not load the report. Please try again later.</p>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 1rem;">
                    ${error.message}
                </p>
            </div>
        `;
        contentEl.style.display = 'block';
        loadingEl.style.display = 'none';
    }
}

// Load last updated time
async function loadLastUpdated() {
    try {
        const response = await fetch(`${REPORTS_BASE_URL}index.md`);
        const text = await response.text();

        // Extract timestamp from index.md
        const match = text.match(/Last updated: (.+)/);
        if (match) {
            document.getElementById('last-updated').textContent = match[1];
        }
    } catch (error) {
        console.error('Error loading last updated time:', error);
        document.getElementById('last-updated').textContent = 'Unknown';
    }
}

// Share on Twitter/X
function shareOnTwitter() {
    const url = window.location.href;
    const text = getShareText();
    const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
    window.open(twitterUrl, '_blank', 'width=550,height=420');
}

// Share on LinkedIn
function shareOnLinkedIn() {
    const url = window.location.href;
    const linkedInUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
    window.open(linkedInUrl, '_blank', 'width=550,height=420');
}

// Copy link to clipboard
async function copyLink() {
    const url = window.location.href;
    try {
        await navigator.clipboard.writeText(url);
        showCopyFeedback();
    } catch (error) {
        console.error('Error copying to clipboard:', error);
        // Fallback for older browsers
        fallbackCopyToClipboard(url);
    }
}

// Show copy feedback
function showCopyFeedback() {
    const copyBtn = document.querySelector('.share-btn.copy');
    const originalText = copyBtn.innerHTML;

    copyBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        Copied!
    `;
    copyBtn.style.background = 'var(--success-color)';

    setTimeout(() => {
        copyBtn.innerHTML = originalText;
        copyBtn.style.background = '';
    }, 2000);
}

// Fallback copy method for older browsers
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        document.execCommand('copy');
        showCopyFeedback();
    } catch (error) {
        console.error('Fallback copy failed:', error);
        alert('Failed to copy link. Please copy manually: ' + text);
    }

    document.body.removeChild(textArea);
}

// Generate share text based on current report
function getShareText() {
    const reportNames = {
        'bob-weekly': 'Bob',
        'erik-weekly': 'Erik',
        'gptme-team-weekly': 'gptme Team'
    };

    const name = reportNames[currentReport] || 'My';
    return `Check out ${name}'s weekly activity on GitHub! 📊`;
}

// Configure marked options
marked.setOptions({
    breaks: true,
    gfm: true
});
