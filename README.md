# What Did You Get Done?

A simple tool to generate activity reports from GitHub, inspired by Elon Musk's "What did you get done this week?" question. Perfect for team leads and managers who want to track progress and achievements.

## Features

- Generate activity reports for individual GitHub users
- Create team activity summaries
- Export reports in Markdown format
- Easy sharing and review
- Automatic dependency management with uv

## Installation

The script uses uv's inline script metadata for dependency management, so you only need:

1. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Set up GitHub token:
```bash
export GITHUB_TOKEN=your_token_here
```

That's it! The script will automatically manage its own dependencies.

## Usage

### Individual Report

```bash
./whatdidyougetdone.py report username
```

Options:
- `--days N`: Look back N days (default: 7)
- `--output FILE`: Specify output file

### Team Report

```bash
./whatdidyougetdone.py team username1 username2 username3
```

Options:
- `--days N`: Look back N days (default: 7)

## Example Output

```markdown
# What did erikbjare get done?

Activity report for the last 7 days:

## ErikBjare/gptme
- 💻 feat: add RAG support
- 🔀 Implement context management (#59)

## ActivityWatch/activitywatch
- 💻 fix: improve error handling
- 💻 docs: update installation instructions
```

## Development

The script is designed to be standalone with its dependencies managed by uv. To develop:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whatdidyougetdone.git
cd whatdidyougetdone
```

2. Make the script executable:
```bash
chmod +x whatdidyougetdone.py
```

3. Run directly:
```bash
./whatdidyougetdone.py
```

Dependencies will be automatically managed in an isolated environment.

## License

MIT License
