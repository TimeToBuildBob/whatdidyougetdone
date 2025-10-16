# What Did You Get Done?

A simple tool to generate activity reports from GitHub and local activity data, inspired by Elon Musk's "What did you get done this week?" question. Perfect for team leads, managers, and anyone who wants to track and showcase their progress and achievements.

## Features

- 📊 Generate activity reports for individual GitHub users
- 👥 Create team activity summaries
- 📁 Export reports in Markdown format
- 🌐 Web UI for easy viewing and sharing
- 📈 Automated weekly report generation (GitHub Pages)
- 💻 ActivityWatch integration for local activity tracking (optional)
- 🎯 Smart filtering of noise and merge commits
- 🎨 Dark/light mode support in web UI
- 📱 Responsive design for mobile and desktop

## Quick Start

### Option 1: Web UI

Visit the live demo at: `https://erikbjare.github.io/whatdidyougetdone/`

The web UI allows you to:
- Enter any GitHub username to generate a report
- View team reports
- Toggle between dark/light mode
- Share reports easily

### Option 2: CLI Tool

The script uses uv's inline script metadata for dependency management.

1. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Set up GitHub token:
```bash
export GITHUB_TOKEN=your_token_here
```

3. Run the tool:
```bash
./whatdidyougetdone.py report username
```

## Usage

### Individual Report

Generate a report for a single user:

```bash
./whatdidyougetdone.py report username
```

Options:
- `--days N`: Look back N days (default: 7)
- `--output FILE`: Save to file (default: stdout)
- `--activitywatch`: Include local ActivityWatch data (requires ActivityWatch)

Example:
```bash
# Generate last 14 days for erikbjare
./whatdidyougetdone.py report erikbjare --days 14

# Save to file
./whatdidyougetdone.py report erikbjare --output report.md

# Include local activity data
./whatdidyougetdone.py report erikbjare --activitywatch
```

### Team Report

Generate a combined report for multiple team members:

```bash
./whatdidyougetdone.py team username1 username2 username3
```

Options:
- `--days N`: Look back N days (default: 7)
- `--output FILE`: Save to file

Example:
```bash
# Generate team report for gptme contributors
./whatdidyougetdone.py team ErikBjare TimeToBuildBob --days 7
```

### Custom Date Range

Specify exact date ranges:

```bash
./whatdidyougetdone.py report username --start 2024-01-01 --end 2024-01-31
```

## Example Output

```markdown
# What did erikbjare get done?

Activity report for the last 7 days:

## ErikBjare/gptme
- ✅ feat: add RAG support (#123)
- 🔄 Implement context management (#59)
- 💻 fix: improve error handling

## ActivityWatch/activitywatch
- ✅ docs: update installation instructions
- 💻 feat: add new visualization
```

## ActivityWatch Integration

[ActivityWatch](https://activitywatch.net/) is a privacy-preserving time tracker that runs locally on your machine. The integration allows you to combine GitHub activity with local development activity for a complete picture.

### Setup

1. Install and run ActivityWatch:
```bash
# See https://activitywatch.net/ for installation
```

2. Generate reports with local data:
```bash
./whatdidyougetdone.py report username --activitywatch
```

### What's Included

- Editor activity (VSCode, Vim, etc.)
- Application usage
- Project time breakdown
- Local commits and file changes

### Privacy

All ActivityWatch data stays on your local machine. The tool only accesses data you explicitly request, and nothing is sent to external servers.

## Automated Reports

The project includes automated weekly report generation via GitHub Actions.

### Setup for Your Repo

1. Fork this repository
2. Add `GITHUB_TOKEN` secret with read permissions
3. Enable GitHub Pages (Settings → Pages → Deploy from branch: `gh-pages`)
4. Reports will be automatically generated weekly

### Manual Trigger

You can manually trigger report generation from the Actions tab.

### Available Reports

- Individual reports for configured users
- Team reports for configured teams
- Customizable date ranges
- Automatic gh-pages deployment

## Web UI

The project includes a modern, responsive web interface for viewing reports.

### Features

- 🌐 No backend required (static HTML/CSS/JS)
- 🎨 Dark/light mode toggle
- 📱 Mobile-friendly responsive design
- 🔍 Real-time GitHub API integration
- 📤 Easy sharing via URL

### Local Development

Open `index.html` in your browser, or use a simple HTTP server:

```bash
python -m http.server 8000
# Open http://localhost:8000
```

### Deployment

The web UI is automatically deployed to GitHub Pages via the `generate-reports.yml` workflow.

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/TimeToBuildBob/whatdidyougetdone.git
cd whatdidyougetdone
```

2. Make the script executable:
```bash
chmod +x whatdidyougetdone.py
```

3. Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
# Linting and type checking
pre-commit run --all-files

# Manual checks
ruff check whatdidyougetdone.py
mypy whatdidyougetdone.py
```

### Dependencies

The script uses uv's inline script metadata, which automatically manages:
- `PyGithub` - GitHub API client
- `aw-client` - ActivityWatch client (optional)

Dependencies are isolated and managed automatically by uv.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Areas for Contribution

- Additional data sources (GitLab, Bitbucket, etc.)
- Enhanced ActivityWatch integration
- Report templates and formatting options
- Web UI improvements
- Documentation improvements

### Guidelines

1. Follow the existing code style (enforced by ruff/mypy)
2. Add tests for new features
3. Update documentation
4. Keep the script standalone and minimal

## API Documentation

### Core Functions

#### `fetch_user_activity(username: str, days: int = 7) -> dict`
Fetches GitHub activity for a user over the specified number of days.

**Returns**: Dictionary with activity data including:
- `repos`: Dictionary of repositories with their events
- `total_events`: Total number of events
- `date_range`: Start and end dates

#### `generate_report(username: str, days: int = 7, output: str = None) -> str`
Generates a formatted Markdown report.

**Parameters**:
- `username`: GitHub username
- `days`: Number of days to look back
- `output`: Optional file path to save report

**Returns**: Markdown-formatted report string

#### `fetch_activitywatch_data(username: str, days: int = 7) -> dict`
Fetches local ActivityWatch data (requires ActivityWatch running).

**Returns**: Dictionary with local activity data including:
- `total_time`: Total tracked time
- `projects`: Time spent per project
- `editors`: Editor usage statistics

### CLI Interface

The tool provides a simple CLI using Python's argparse:

```python
# Report command
whatdidyougetdone.py report <username> [options]

# Team command
whatdidyougetdone.py team <username1> <username2> ... [options]
```

See `--help` for full options.

## FAQ

### Q: Do I need a GitHub token?

A: Yes, for CLI usage. The web UI makes requests from the browser, so it uses the visitor's IP limits.

### Q: How do I get a GitHub token?

A: Visit GitHub Settings → Developer settings → Personal access tokens → Generate new token. Only public repository read access is needed.

### Q: Can I use this for private repositories?

A: Yes, if you grant the appropriate permissions to your GitHub token.

### Q: Does this work with GitLab/Bitbucket?

A: Not currently, but contributions are welcome!

### Q: Is my data private?

A: Yes! ActivityWatch data stays local, and GitHub data is fetched directly from GitHub's API using your token.

## License

MIT License - see LICENSE file for details.

## Credits

Inspired by Elon Musk's famous question: "What did you get done this week?"

Built with:
- Python 3.10+
- PyGithub for GitHub API
- ActivityWatch for local tracking
- GitHub Actions for automation
- Pure HTML/CSS/JS for web UI

## Links

- [GitHub Repository](https://github.com/TimeToBuildBob/whatdidyougetdone)
- [Live Demo](https://erikbjare.github.io/whatdidyougetdone/)
- [ActivityWatch](https://activitywatch.net/)
- [Issue Tracker](https://github.com/TimeToBuildBob/whatdidyougetdone/issues)
