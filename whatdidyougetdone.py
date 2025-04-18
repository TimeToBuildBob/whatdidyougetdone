#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "PyGithub>=2.1.1",
#   "click>=8.1.7",
# ]
# [tool.uv]
# exclude-newer = "2024-01-01T00:00:00Z"
# ///
#
# What Did You Get Done? - Activity report generator
# Usage:
#   ./whatdidyougetdone.py report <username>
#   ./whatdidyougetdone.py team <username1> <username2> ...

import click
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
from typing import Optional
import sys
import webbrowser
from github import Github

# Get script directory
SCRIPT_DIR = Path(__file__).parent.absolute()


def preview_in_browser(filename: Path) -> None:
    """Open file in browser if in interactive mode."""
    if sys.stdout.isatty():
        if click.confirm("Open in browser?"):
            webbrowser.open(f"file://{filename.absolute()}")


def get_github_token() -> str:
    """Get GitHub token from environment or GitHub CLI."""
    # Try environment variable first
    if token := os.getenv("GITHUB_TOKEN"):
        return token

    # Try GitHub CLI
    try:
        import subprocess

        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass

    print("Could not get GitHub token from environment or gh CLI")
    print("Please either:")
    print("1. Install GitHub CLI and authenticate with 'gh auth login', or")
    print("2. Set GITHUB_TOKEN environment variable")
    print("You can create a token at: https://github.com/settings/tokens")
    print("Required scopes: repo, read:user")
    exit(1)


def setup_github():
    """Ensure GitHub token is available."""
    token = get_github_token()
    os.environ["GITHUB_TOKEN"] = token  # Set for Github instance


def get_user_activity(username: str, days: int = 7):
    """Get GitHub activity for a user over the last N days."""
    g = Github(os.getenv("GITHUB_TOKEN"))
    user = g.get_user(username)

    # Calculate date range (in UTC)
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)

    # Get all events
    activities = []
    for event in user.get_events():
        if event.created_at < start_date:
            break

        # Format based on event type
        if event.type == "PushEvent":
            for commit in event.payload["commits"]:
                activities.append(
                    {
                        "type": "commit",
                        "repo": event.repo.name,
                        "message": commit["message"],
                        "date": event.created_at,
                    }
                )
        elif event.type == "PullRequestEvent":
            activities.append(
                {
                    "type": "pr",
                    "repo": event.repo.name,
                    "title": event.payload["pull_request"]["title"],
                    "state": event.payload["pull_request"]["state"],
                    "date": event.created_at,
                }
            )
        # Add more event types as needed

    return activities


def generate_report(username: str, days: int = 7):
    """Generate a markdown report of user activity."""
    activities = get_user_activity(username, days)

    # Group by repo
    repos: dict[str, list[dict]] = {}
    for activity in activities:
        repo = activity["repo"]
        if repo not in repos:
            repos[repo] = []
        repos[repo].append(activity)

    # Generate markdown
    report = f"# What did {username} get done?\n\n"
    report += f"Activity report for the last {days} days:\n\n"

    for repo, acts in repos.items():
        report += f"## {repo}\n\n"
        # Group by type
        commits = [act for act in acts if act["type"] == "commit"]
        prs = [act for act in acts if act["type"] == "pr"]

        # Show PRs first (higher level changes)
        for act in sorted(prs, key=lambda x: x["date"], reverse=True):
            report += f"- 🔀 {act['title']} ({act['state']})\n"

        # Then show commits
        for act in sorted(commits, key=lambda x: x["date"], reverse=True):
            # Skip merge commits and commits that are part of PRs
            if act["message"].startswith("Merge") or "Co-authored-by" in act["message"]:
                continue
            report += f"- 💻 {act['message']}\n"

    return report


def save_report(username: str, report: str) -> Path:
    """Save report to file."""
    reports_dir = SCRIPT_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)

    filename = reports_dir / f"{username}-{datetime.now().strftime('%Y-%m-%d')}.md"
    filename.write_text(report)
    return filename


@click.group()
def cli():
    """What did you get done? - Activity report generator"""
    pass


@cli.command()
@click.argument("username")
@click.option("--days", default=7, help="Number of days to look back")
@click.option("--output", help="Output file (default: reports/<username>-<date>.md)")
def report(username: str, days: int, output: Optional[str]):
    """Generate activity report for a GitHub user"""
    setup_github()

    # Generate report
    report_text = generate_report(username, days)

    # Save report
    if output:
        filename = Path(output)
    else:
        filename = save_report(username, report_text)

    print(f"Report saved to: {filename}")
    preview_in_browser(filename)


@cli.command()
@click.argument("usernames", nargs=-1)
@click.option("--days", default=7, help="Number of days to look back")
def team(usernames: tuple[str], days: int):
    """Generate team activity report"""
    setup_github()

    # Generate combined report
    report = "# Team Activity Report\n\n"
    report += f"Activity for the last {days} days\n\n"

    for username in usernames:
        activities = get_user_activity(username, days)
        report += f"## {username}\n\n"

        # Count activities
        commit_count = sum(1 for a in activities if a["type"] == "commit")
        pr_count = sum(1 for a in activities if a["type"] == "pr")

        report += f"- 💻 {commit_count} commits\n"
        report += f"- 🔀 {pr_count} pull requests\n\n"

        # Add details
        for activity in sorted(activities, key=lambda x: x["date"], reverse=True):
            if activity["type"] == "commit":
                report += f"- [{activity['repo']}] {activity['message']}\n"
            elif activity["type"] == "pr":
                report += f"- [{activity['repo']}] {activity['title']} ({activity['state']})\n"
        report += "\n"

    # Save report
    reports_dir = SCRIPT_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)

    filename = reports_dir / f"team-{datetime.now().strftime('%Y-%m-%d')}.md"
    filename.write_text(report)

    print(f"Team report saved to: {filename}")
    preview_in_browser(filename)


if __name__ == "__main__":
    cli()
