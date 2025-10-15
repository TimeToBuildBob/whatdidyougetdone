#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "PyGithub>=2.1.1",
#   "click>=8.1.7",
#   "aw-client>=0.5.13",
# ]
# [tool.uv]
# exclude-newer = "2024-10-01T00:00:00Z"
# ///
#
# What Did You Get Done? - Activity report generator with ActivityWatch integration
# Usage:
#   ./whatdidyougetdone.py report <username>
#   ./whatdidyougetdone.py report <username> --activitywatch  # Include local activity data

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


def get_aw_activity(days: int = 7):
    """Get ActivityWatch activity data for the last N days."""
    try:
        from aw_client import ActivityWatchClient
    except ImportError:
        print("Warning: aw-client not available. Install with: pip install aw-client")
        return None

    try:
        # Connect to ActivityWatch
        aw = ActivityWatchClient("whatdidyougetdone", testing=False)

        # Calculate date range
        end_date = datetime.now(timezone.utc)
        start_date = start_of_day(end_date - timedelta(days=days))

        # Get buckets for window activity
        buckets = aw.get_buckets()
        window_buckets = [bid for bid in buckets.keys() if "window" in bid.lower()]

        if not window_buckets:
            print("Warning: No ActivityWatch window buckets found")
            return None

        # Query for activity data
        # Get top applications and projects
        query = f"""
        events = flood(query_bucket(find_bucket("{window_buckets[0]}")));
        events = filter_period_intersect(events, {start_date.isoformat()}, {end_date.isoformat()});
        events = merge_events_by_keys(events, ["app", "title"]);
        events = sort_by_duration(events);
        RETURN = {{"apps": events[:10]}};
        """

        result = aw.query(query)[0]

        # Calculate total time
        total_time = sum(e["duration"] for e in result.get("apps", []))

        return {
            "total_hours": total_time / 3600,
            "apps": result.get("apps", [])[:5],  # Top 5 apps
            "start_date": start_date,
            "end_date": end_date,
        }

    except Exception as e:
        print(f"Warning: Could not fetch ActivityWatch data: {e}")
        return None


def setup_github():
    """Ensure GitHub token is available."""
    token = get_github_token()
    os.environ["GITHUB_TOKEN"] = token


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
    max_events = 1000

    try:
        for event in user.get_events():
            events_checked += 1
            if events_checked > max_events:
                print(
                    f"Note: Limited to checking {max_events} recent events for {username}"
                )
                break
            if event.created_at < start_date:
                break

            if event.type == "PushEvent":
                repo_name = event.repo.name
                for commit in event.payload.get("commits", []):
                    activities.append(
                        {
                            "type": "commit",
                            "repo": repo_name,
                            "message": commit.get("message", ""),
                            "sha": commit.get("sha", "")[:7],
                            "date": event.created_at,
                        }
                    )
            elif event.type == "PullRequestEvent":
                pr = event.payload.get("pull_request", {})
                state = pr.get("state", "unknown")
                if event.payload.get("action") == "closed" and pr.get("merged"):
                    state = "merged"

                activities.append(
                    {
                        "type": "pr",
                        "repo": event.repo.name,
                        "title": pr.get("title", ""),
                        "state": state,
                        "number": pr.get("number", 0),
                        "date": event.created_at,
                    }
                )

    except Exception as e:
        print(f"Error fetching GitHub activity: {e}")

    return sorted(activities, key=lambda x: x["date"], reverse=True)


def generate_report(
    username: str,
    days: int = 7,
    include_timeline: bool = False,
    include_aw: bool = False,
):
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
    report += f"- 📦 {active_repos} active repositories\n"

    # Add ActivityWatch data if available
    if include_aw:
        aw_data = get_aw_activity(days)
        if aw_data:
            report += f"- ⏱️ {aw_data['total_hours']:.1f} hours of local activity\n"

    report += "\n"

    # ActivityWatch section
    if include_aw:
        aw_data = get_aw_activity(days)
        if aw_data and aw_data["apps"]:
            report += "## Local Activity (via ActivityWatch)\n\n"
            report += "Top applications by time:\n\n"
            for app in aw_data["apps"]:
                app_name = app["data"].get("app", "Unknown")
                hours = app["duration"] / 3600
                report += f"- 💻 {app_name}: {hours:.1f}h\n"
            report += "\n"

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
        commits = [act for act in acts if act["type"] == "commit"]
        prs = [act for act in acts if act["type"] == "pr"]

        for act in sorted(prs, key=lambda x: x["date"], reverse=True):
            report += f"- 🔀 {act['title']} ({act['state']})\n"

        for act in sorted(commits, key=lambda x: x["date"], reverse=True):
            if act["message"].startswith("Merge") or "Co-authored-by" in act["message"]:
                continue
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
    """What Did You Get Done? - Activity report generator"""
    setup_github()


@cli.command()
@click.argument("username")
@click.option("--days", default=7, help="Number of days to look back")
@click.option("--file", help="Save output to file instead of stdout")
@click.option("--timeline", is_flag=True, help="Include detailed timeline")
@click.option("--activitywatch", is_flag=True, help="Include local ActivityWatch data")
def report(
    username: str, days: int, file: Optional[str], timeline: bool, activitywatch: bool
):
    """Generate activity report for a single user"""
    report_text = generate_report(
        username, days, include_timeline=timeline, include_aw=activitywatch
    )

    if file:
        with open(file, "w") as f:
            f.write(report_text)
        print(f"Report saved to {file}")
    else:
        print(report_text)


@cli.command()
@click.argument("usernames", nargs=-1)
@click.option("--days", default=7, help="Number of days to look back")
@click.option("--file", help="Save output to file instead of stdout")
@click.option("--timeline", is_flag=True, help="Include detailed timeline")
def team(usernames: tuple[str], days: int, file: Optional[str], timeline: bool):
    """Generate combined activity report for multiple users"""
    if not usernames:
        print("Error: Please provide at least one username")
        return

    report_text = "# Team Activity Report\n\n"
    report_text += f"Activity for the last {days} days:\n\n"

    for username in usernames:
        print(f"Fetching activity for {username}...")
        user_report = generate_report(
            username, days, include_timeline=timeline, include_aw=False
        )
        # Remove the title and first line from individual reports
        lines = user_report.split("\n")
        report_text += "\n".join(lines[2:]) + "\n---\n\n"

    if file:
        with open(file, "w") as f:
            f.write(report_text)
        print(f"Report saved to {file}")
    else:
        print(report_text)


if __name__ == "__main__":
    cli()
