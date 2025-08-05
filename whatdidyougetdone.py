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

import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import click
from github import Github

# Get script directory
SCRIPT_DIR = Path(__file__).parent.absolute()


def start_of_day(dt: datetime) -> datetime:
    """Get the start of the day for a given datetime (with offset for past-midnight but pre-4AM activity to count to previous day)."""
    return dt.replace(hour=4, minute=0, second=0, microsecond=0)


def get_github_token() -> str:
    """Get GitHub token from environment or GitHub CLI."""
    # Try environment variable first
    if token := os.getenv("GITHUB_TOKEN"):
        return token

    # Try GitHub CLI
    try:
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
    start_date = start_of_day(end_date - timedelta(days=days))

    # Warn about GitHub API limitations
    if days > 90:
        print("Warning: GitHub Events API only returns events from the last 90 days.")
        print(f"Requested {days} days, but will only get events from the last 90 days.")
        print(
            f"Effective date range: {(end_date - timedelta(days=90)).strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        )
        print()

    # Get events with pagination
    activities = []
    events_checked = 0
    max_events = 1000  # Reasonable limit to prevent excessive API calls

    try:
        for event in user.get_events():
            events_checked += 1

            # Break if we've checked too many events (rate limiting protection)
            if events_checked > max_events:
                print(
                    f"Note: Limited to checking {max_events} recent events for {username}"
                )
                break

            # Break if event is too old
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

    except Exception as e:
        print(f"Warning: Error fetching events for {username}: {e}")
        print(f"Proceeding with {len(activities)} activities found so far...")

    # Debug information
    if activities:
        oldest_activity = min(activities, key=lambda x: x["date"])
        newest_activity = max(activities, key=lambda x: x["date"])
        print(f"Found {len(activities)} activities for {username}")
        print(
            f"Date range: {oldest_activity['date'].strftime('%Y-%m-%d')} to {newest_activity['date'].strftime('%Y-%m-%d')}"
        )
        print(f"Checked {events_checked} events total")

        if events_checked >= max_events:
            print(
                f"Hit the {max_events} event limit - some recent activity may be missing"
            )
        elif len(activities) >= 300:
            print("Note: GitHub Events API has a 300 event maximum limit")
        print()
    else:
        print(f"No activities found for {username} in the requested time range")
        print()

    return activities


def generate_report(username: str, days: int = 7, include_timeline: bool = False):
    """Generate a markdown report of user activity."""
    activities = get_user_activity(username, days)

    # Calculate summary stats
    total_commits = sum(1 for a in activities if a["type"] == "commit")
    total_prs = sum(1 for a in activities if a["type"] == "pr")
    active_repos = len({a["repo"] for a in activities})

    # Generate markdown
    report = f"# What did {username} get done?\n\n"
    report += f"Activity report for the last {days} days:\n\n"

    # Summary stats
    report += "## Summary\n\n"
    report += f"- 💻 {total_commits} commits\n"
    report += f"- 🔀 {total_prs} pull requests\n"
    report += f"- 📦 {active_repos} active repositories\n\n"

    # Group by repo
    repos: dict[str, list[dict]] = {}
    for activity in activities:
        repo = activity["repo"]
        if repo not in repos:
            repos[repo] = []
        repos[repo].append(activity)

    # Activity by repo
    report += "## Activity by Repository\n\n"
    for repo, acts in repos.items():
        report += f"### {repo}\n\n"
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
            # Take only first line of commit message
            message = act["message"].split("\n")[0]
            report += f"- 💻 {message}\n"

    # Optional timeline
    if include_timeline:
        report += "\n<details><summary>Detailed Timeline</summary>\n\n"
        for act in sorted(activities, key=lambda x: x["date"], reverse=True):
            date_str = act["date"].strftime("%Y-%m-%d %H:%M")
            if act["type"] == "commit":
                message = act["message"].split("\n")[0]
                report += f"- {date_str} 💻 [{act['repo']}] {message}\n"
            elif act["type"] == "pr":
                report += (
                    f"- {date_str} 🔀 [{act['repo']}] {act['title']} ({act['state']})\n"
                )
        report += "\n</details>\n"

    return report


@click.group()
def cli():
    """What did you get done? - Activity report generator"""
    pass


@cli.command()
@click.argument("username")
@click.option("--days", default=7, help="Number of days to look back")
@click.option("--file", help="Save output to file instead of stdout")
@click.option("--timeline", is_flag=True, help="Include detailed timeline")
def report(username: str, days: int, file: Optional[str], timeline: bool):
    """Generate activity report for a GitHub user"""
    setup_github()

    # Generate report
    report_text = generate_report(username, days, include_timeline=timeline)

    # Output report
    if file:
        Path(file).write_text(report_text)
        print(f"Report saved to: {file}")
    else:
        print(report_text)


@cli.command()
@click.argument("usernames", nargs=-1)
@click.option("--days", default=7, help="Number of days to look back")
@click.option("--file", help="Save output to file instead of stdout")
@click.option("--timeline", is_flag=True, help="Include detailed timeline")
def team(usernames: tuple[str], days: int, file: Optional[str], timeline: bool):
    """Generate team activity report"""
    setup_github()

    # Generate combined report
    report = "# Team Activity Report\n\n"
    report += f"Activity for the last {days} days\n\n"

    # Team summary
    total_team_commits = 0
    total_team_prs = 0
    active_repos: set[str] = set()

    # Collect all activities first
    all_activities: list[tuple[str, dict]] = []
    for username in usernames:
        activities = get_user_activity(username, days)
        all_activities.extend((username, a) for a in activities)

        # Update team stats
        commit_count = sum(1 for a in activities if a["type"] == "commit")
        pr_count = sum(1 for a in activities if a["type"] == "pr")
        active_repos.update(a["repo"] for a in activities)

        total_team_commits += commit_count
        total_team_prs += pr_count

    # Team summary
    report += "## Team Summary\n\n"
    report += f"- 👥 {len(usernames)} team members\n"
    report += f"- 💻 {total_team_commits} commits\n"
    report += f"- 🔀 {total_team_prs} pull requests\n"
    report += f"- 📦 {len(active_repos)} active repositories\n\n"

    # Per-user summary
    for username in usernames:
        user_activities = [a for u, a in all_activities if u == username]
        report += f"## {username}\n\n"

        # User stats
        commit_count = sum(1 for a in user_activities if a["type"] == "commit")
        pr_count = sum(1 for a in user_activities if a["type"] == "pr")
        user_repos = len({a["repo"] for a in user_activities})

        report += f"- 💻 {commit_count} commits\n"
        report += f"- 🔀 {pr_count} pull requests\n"
        report += f"- 📦 {user_repos} active repositories\n\n"

        # Group by repo
        repos: dict[str, list[dict]] = {}
        for activity in user_activities:
            repo = activity["repo"]
            if repo not in repos:
                repos[repo] = []
            repos[repo].append(activity)

        for repo, acts in repos.items():
            report += f"### {repo}\n\n"
            # Group by type
            commits = [act for act in acts if act["type"] == "commit"]
            prs = [act for act in acts if act["type"] == "pr"]

            # Show PRs first
            for act in sorted(prs, key=lambda x: x["date"], reverse=True):
                report += f"- 🔀 {act['title']} ({act['state']})\n"

            # Then commits
            for act in sorted(commits, key=lambda x: x["date"], reverse=True):
                if (
                    act["message"].startswith("Merge")
                    or "Co-authored-by" in act["message"]
                ):
                    continue
                message = act["message"].split("\n")[0]
                report += f"- 💻 {message}\n"
            report += "\n"

    # Optional timeline
    if timeline:
        report += "\n<details><summary>Team Timeline</summary>\n\n"
        for username, act in sorted(
            all_activities, key=lambda x: x[1]["date"], reverse=True
        ):
            date_str = act["date"].strftime("%Y-%m-%d %H:%M")
            if act["type"] == "commit":
                message = act["message"].split("\n")[0]
                report += f"- {date_str} 💻 {username} [{act['repo']}] {message}\n"
            elif act["type"] == "pr":
                report += f"- {date_str} 🔀 {username} [{act['repo']}] {act['title']} ({act['state']})\n"
        report += "\n</details>\n"

    # Output report
    if file:
        Path(file).write_text(report)
        print(f"Report saved to: {file}")
    else:
        print(report)


if __name__ == "__main__":
    cli()
