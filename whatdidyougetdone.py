#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = [
#   "PyGithub>=2.1.1",
#   "click>=8.1.7",
#   "platformdirs>=4.1.0",
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
import json
import os
from pathlib import Path
from typing import Optional
from github import Github
from platformdirs import user_config_dir

# Define app name and author for config directory
APP_NAME = "whatdidyougetdone"
APP_AUTHOR = "brayo"

def get_config_dir() -> Path:
    """Get the platform-specific config directory."""
    config_dir = Path(user_config_dir(APP_NAME, APP_AUTHOR))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def get_github_token() -> str:
    """
    Get GitHub token from config file or environment.
    Updates config file if token is in environment.
    Exits if no token is found.
    """
    config_file = get_config_dir() / ".env"
    
    # Try reading from config file first
    if config_file.exists():
        with open(config_file) as f:
            for line in f:
                if line.startswith('GITHUB_TOKEN='):
                    return line.split('=')[1].strip()
    
    # Check environment variable
    token = os.getenv("GITHUB_TOKEN")
    if token:
        # Save to config file for future use
        with open(config_file, 'w') as f:
            f.write(f"GITHUB_TOKEN={token}\n")
        return token
    
    # No token found
    print("GitHub token not found!")
    print("Either:")
    print(f"1. Create {config_file} with GITHUB_TOKEN=your_token")
    print("2. Set GITHUB_TOKEN environment variable")
    print("\nYou can create a token at: https://github.com/settings/tokens")
    print("Required scopes: repo, read:user")
    exit(1)

# Get script directory
SCRIPT_DIR = Path(__file__).parent.absolute()


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

def preview_in_browser(filename: Path):
    """Open file in browser if in interactive mode."""
    if sys.stdout.isatty():
        if click.confirm("Open in browser?"):
            webbrowser.open(f"file://{os.path.abspath(filename)}")


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
            # Only process commits if:
            # 1. The push was by the user we're interested in
            # 2. If it's a fork, only include commits not from parent repo
            if event.actor.login == username:
                # Get repo info to check if it's a fork
                repo_info = json.loads(os.popen(f'gh repo view {event.repo.name} --json isFork,parent').read())
                
                # For forks, skip showing commits if they're in the parent
                if repo_info.get('isFork', False):
                    parent_repo = repo_info['parent']
                    parent_name = f"{parent_repo['owner']['login']}/{parent_repo['name']}"
                    
                    # If user has access to parent repo, show commits there instead
                    try:
                        os.popen(f'gh repo view {parent_name}').read()
                        # User has access, skip showing in fork
                        continue
                    except:
                        # User doesn't have access to parent, show in fork
                        for commit in event.payload["commits"]:
                            activities.append({
                                "type": "commit",
                                "repo": event.repo.name,
                                "message": commit["message"],
                                "date": event.created_at,
                                "author": commit["author"],
                                "sha": commit["sha"]
                            })
                else:
                    # For non-forks, include all commits
                    for commit in event.payload["commits"]:
                        # Get commit stats from GitHub API
                        try:
                            stats_output = os.popen(f'gh api repos/{event.repo.name}/commits/{commit["sha"]}').read()
                            commit_data = json.loads(stats_output)
                            activities.append({
                                "type": "commit",
                                "repo": event.repo.name,
                                "message": commit["message"],
                                "date": event.created_at,
                                "author": commit["author"],
                                "sha": commit["sha"],
                                "stats": commit_data.get("stats", {})
                            })
                        except:
                            # If we can't get stats, add commit without them
                            activities.append({
                                "type": "commit",
                                "repo": event.repo.name,
                                "message": commit["message"],
                                "date": event.created_at,
                                "author": commit["author"],
                                "sha": commit["sha"]
                            })
        elif event.type == "PullRequestEvent":
            pr = event.payload["pull_request"]
            base_repo = pr["base"]["repo"]["full_name"]
            head_repo = pr["head"]["repo"]["full_name"]
            
            # Include PR if:
            # 1. User created the PR (regardless of target)
            # 2. PR is targeting user's repo
            pr_author = pr["user"]["login"]
            base_owner = pr["base"]["repo"]["owner"]["login"]
            
            if pr_author == username or base_owner == username:
                activities.append({
                    "type": "pr",
                    "repo": base_repo,
                    "title": pr["title"],
                    "state": pr["state"],
                    "date": event.created_at,
                    "head_repo": head_repo,
                    "author": pr_author
                })
        # Add more event types as needed

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
    
    # Calculate date range
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)
    
    # Generate markdown
    report = f"# What did {username} get done?\n\n"
    report += f"Activity from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}:\n\n"
    
    # Add summary if there's activity
    if activities:
        total_commits = len({a["sha"] for a in activities if a["type"] == "commit"})
        total_prs = len({(a["repo"], a["title"]) for a in activities if a["type"] == "pr"})
        report += f"Summary:\n"
        report += f"- 💻 {total_commits} unique commits\n"
        report += f"- 🔀 {total_prs} pull requests\n\n"
    else:
        report += "No activity found in this time period.\n\n"
    
    # Sort repos by activity date
    sorted_repos = sorted(
        repos.items(),
        key=lambda x: max((act["date"] for act in x[1])),
        reverse=True
    )
    
    for repo, acts in sorted_repos:
        # Get repo info
        repo_info = json.loads(os.popen(f'gh repo view {repo} --json isFork,parent').read())
        
        # Format repo header
        if repo_info.get('isFork', False):
            parent = repo_info['parent']
            report += f"## {repo} (fork of {parent['owner']['login']}/{parent['name']})\n\n"
        else:
            report += f"## {repo}\n\n"
        
        # Group by type
        commits = [act for act in acts if act["type"] == "commit"]
        prs = [act for act in acts if act["type"] == "pr"]
        
        # Skip PRs in fork if they target parent
        if repo_info.get('isFork', False):
            prs = [pr for pr in prs if pr["head_repo"] == repo]
        
        # Group PRs by title
        pr_groups = {}
        for pr in prs:
            title = pr['title']
            if title not in pr_groups:
                pr_groups[title] = {'date': pr['date'], 'states': set()}
            pr_groups[title]['states'].add(pr['state'])
            # Keep the most recent date
            if pr['date'] > pr_groups[title]['date']:
                pr_groups[title]['date'] = pr['date']
        
        # Show PRs first (higher level changes)
        for title, info in sorted(pr_groups.items(), key=lambda x: x[1]['date'], reverse=True):
            states = info['states']
            status = "✅" if "closed" in states else "🔄"
            report += f"- {status} {title}\n"
        
        # Then show commits (deduplicated by SHA)
        seen_shas = set()
        for act in sorted(commits, key=lambda x: x["date"], reverse=True):
            # Skip merge commits and commits that are part of PRs
            if act["message"].startswith("Merge") or "Co-authored-by" in act["message"]:
                continue
            
            if act["sha"] not in seen_shas:
                seen_shas.add(act["sha"])
                # Get first line of commit message for display
                message = act["message"].split('\n')[0].strip()
                short_sha = act["sha"][:7]  # First 7 chars of SHA
                
                # Format additions/deletions stats
                stats = ""
                if "stats" in act:
                    adds = act["stats"].get("additions", 0)
                    dels = act["stats"].get("deletions", 0)
                    if adds or dels:
                        stats = f"<span style=\"color: #28a745\">+{adds}</span><span style=\"color: #dc3545\">-{dels}</span>"
                
                report += f"- 💻 {message} ({short_sha}){stats}\n"
    
    return report

def save_report(username: str, report: str) -> Path:
    """Save report to file."""
    reports_dir = SCRIPT_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)

    filename = reports_dir / f"{username}-{datetime.now().strftime('%Y-%m-%d')}.md"
    filename.write_text(report)
    return Path(filename)

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


        # Add details
        for activity in sorted(activities, key=lambda x: x["date"], reverse=True):
            if activity["type"] == "commit":
                report += f"- [{activity['repo']}] {activity['message']}\n"
            elif activity["type"] == "pr":
                status = "✅" if activity["state"] == "closed" else "🔄"
                report += f"- [{activity['repo']}] {status} {activity['title']}\n"
        report += "\n"

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
