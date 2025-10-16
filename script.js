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

        // Update dynamic OG tags
        updateOpenGraphTags(reportName, markdown);

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

// Update Open Graph meta tags dynamically
function updateOpenGraphTags(reportName, markdown) {
    const reportNames = {
        'bob-weekly': 'Bob',
        'erik-weekly': 'Erik',
        'gptme-team-weekly': 'gptme Team'
    };

    const name = reportNames[reportName] || 'User';
    const stats = extractStats(markdown);

    // Update title
    const titleTag = document.querySelector('meta[property="og:title"]');
    if (titleTag) {
        titleTag.content = `${name}'s Weekly Activity - What Did You Get Done?`;
    }

    // Update description with stats
    const descTag = document.querySelector('meta[property="og:description"]');
    if (descTag) {
        let desc = `${name}'s GitHub activity: `;
        const parts = [];
        if (stats.commits > 0) parts.push(`${stats.commits} commits`);
        if (stats.prs > 0) parts.push(`${stats.prs} PRs`);
        if (stats.repos > 0) parts.push(`${stats.repos} repos`);
        desc += parts.join(', ');
        descTag.content = desc;
    }
}

// Extract stats from markdown content
function extractStats(content) {
    const commitMatch = content.match(/(\d+)\s+commits?/i);
    const prMatch = content.match(/(\d+)\s+pull requests?/i);
    const repoMatch = content.match(/(\d+)\s+active repositories?/i);

    return {
        commits: commitMatch ? parseInt(commitMatch[1]) : 0,
        prs: prMatch ? parseInt(prMatch[1]) : 0,
        repos: repoMatch ? parseInt(repoMatch[1]) : 0
    };
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

// Generate share text with actual stats
function getShareText() {
    const reportNames = {
        'bob-weekly': 'Bob',
        'erik-weekly': 'Erik',
        'gptme-team-weekly': 'gptme Team'
    };

    const name = reportNames[currentReport] || 'My';

    // Parse report content for stats
    const content = document.getElementById('report-content').innerText;
    const stats = extractStats(content);

    // Generate engaging text with stats
    let text = `📊 ${name}'s week in GitHub:\n\n`;

    if (stats.commits > 0) text += `💻 ${stats.commits} commits\n`;
    if (stats.prs > 0) text += `🔀 ${stats.prs} pull requests\n`;
    if (stats.repos > 0) text += `📦 ${stats.repos} active repos\n`;

    text += '\n#WhatDidYouGetDone #GitHub #OpenSource';

    return text;
}

// Show share preview modal
function showSharePreview(platform) {
    const text = getShareText();
    const url = window.location.href;

    // Create modal HTML
    const modalHTML = `
        <div class="share-modal-overlay" id="shareModal">
            <div class="share-modal">
                <div class="share-modal-header">
                    <h3>📢 Share Your Week</h3>
                    <button class="close-modal" onclick="closeShareModal()">✕</button>
                </div>
                <div class="share-modal-body">
                    <label for="shareText">Customize your share text:</label>
                    <textarea id="shareText" rows="8">${text}</textarea>
                    <div class="share-preview">
                        <strong>Link:</strong> ${url}
                    </div>
                </div>
                <div class="share-modal-footer">
                    <button class="btn-secondary" onclick="closeShareModal()">Cancel</button>
                    <button class="btn-primary" onclick="confirmShare('${platform}')">
                        Share on ${platform}
                    </button>
                </div>
            </div>
        </div>
    `;

    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

// Close share modal
function closeShareModal() {
    const modal = document.getElementById('shareModal');
    if (modal) {
        modal.remove();
    }
}

// Confirm and execute share
function confirmShare(platform) {
    const text = document.getElementById('shareText').value;
    const url = window.location.href;

    closeShareModal();

    if (platform === 'Twitter') {
        const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
        window.open(twitterUrl, '_blank', 'width=550,height=420');
    } else if (platform === 'LinkedIn') {
        const linkedInUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
        window.open(linkedInUrl, '_blank', 'width=550,height=420');
    }
}

// Share on Twitter/X with preview
function shareOnTwitter() {
    showSharePreview('Twitter');
}

// Share on LinkedIn with preview
function shareOnLinkedIn() {
    showSharePreview('LinkedIn');
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

// Configure marked options
marked.setOptions({
    breaks: true,
    gfm: true
});

// Team Dashboard functionality
function setupTeamDashboard() {
    const teamForm = document.getElementById('team-form');
    const teamDashboard = document.getElementById('team-dashboard');
    const reportContent = document.getElementById('report-content');
    const shareSection = document.getElementById('share-section');

    // Handle view switching
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            if (btn.dataset.view === 'custom-team') {
                // Show team dashboard
                teamDashboard.style.display = 'block';
                reportContent.style.display = 'none';
                shareSection.style.display = 'none';
                document.getElementById('loading').style.display = 'none';

                // Update active button
                document.querySelectorAll('.nav-btn').forEach(b => {
                    b.classList.remove('active');
                });
                btn.classList.add('active');
            }
        });
    });

    // Handle form submission
    teamForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const usernames = document.getElementById('team-usernames').value
            .split(',')
            .map(u => u.trim())
            .filter(u => u.length > 0);

        const days = parseInt(document.getElementById('team-days').value);
        const startDate = document.getElementById('team-start-date').value;
        const endDate = document.getElementById('team-end-date').value;

        if (usernames.length === 0) {
            alert('Please enter at least one GitHub username');
            return;
        }

        // Show loading
        const resultSection = document.getElementById('team-result');
        const resultContent = document.getElementById('team-content');

        resultContent.innerHTML = `
            <div style="text-align: center; padding: 2rem;">
                <div class="spinner"></div>
                <p>Generating team report...</p>
            </div>
        `;
        resultSection.style.display = 'block';

        // TODO: Implement actual GitHub API calls
        // For now, show a placeholder message
        setTimeout(() => {
            resultContent.innerHTML = `
                <div style="text-align: center; padding: 2rem;">
                    <h3>🚧 Feature Under Development</h3>
                    <p style="margin: 1rem 0;">
                        The dynamic team report generation is currently under development.
                    </p>
                    <p style="color: var(--text-secondary);">
                        <strong>Your request:</strong><br/>
                        Usernames: ${usernames.join(', ')}<br/>
                        Days: ${days}<br/>
                        ${startDate && endDate ? `Date range: ${startDate} to ${endDate}` : ''}
                    </p>
                    <p style="margin-top: 1.5rem; color: var(--text-secondary);">
                        <strong>Next steps for implementation:</strong>
                    </p>
                    <ul style="text-align: left; max-width: 600px; margin: 1rem auto; color: var(--text-secondary);">
                        <li>Add GitHub API authentication (requires user token or backend)</li>
                        <li>Implement client-side GitHub API calls for fetching user activity</li>
                        <li>Parse and aggregate activity data across users</li>
                        <li>Format and display results as markdown</li>
                        <li>Add caching to avoid rate limits</li>
                    </ul>
                    <p style="margin-top: 1.5rem;">
                        <a href="https://github.com/ErikBjare/whatdidyougetdone" target="_blank" class="btn-primary">
                            View Project on GitHub
                        </a>
                    </p>
                </div>
            `;
        }, 1000);
    });
}

// Initialize team dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    setupTeamDashboard();
});
