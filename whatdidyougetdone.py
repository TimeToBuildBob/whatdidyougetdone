#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "PyGithub>=2.1.1",
#   "click>=8.1.7",
#   "aw-client>=0.5.13",
#   "tweepy>=4.14.0",
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


def get_twitter_credentials():
    """Get Twitter API credentials from environment.

    Required environment variables:
    - TWITTER_BEARER_TOKEN: Twitter API Bearer Token

    Returns:
        Twitter API Bearer Token or None if not available
    """
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        print("Warning: TWITTER_BEARER_TOKEN not set. Twitter integration disabled.")
        print("To enable Twitter integration:")
        print("1. Create a Twitter Developer App at https://developer.twitter.com/")
        print("2. Get your Bearer Token from the app dashboard")
        print("3. Set environment variable: export TWITTER_BEARER_TOKEN='your_token'")
        return None
    return bearer_token


def get_twitter_activity(
    username: str,
    days: int = 7,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    """Get Twitter activity data for a user.

    Args:
        username: Twitter username (without @)
        days: Number of days to look back (default 7)
        start_date: Optional start date (UTC)
        end_date: Optional end date (UTC)

    Returns:
        Dictionary with Twitter activity data or None if unavailable
    """
    bearer_token = get_twitter_credentials()
    if not bearer_token:
        return None

    try:
        import tweepy
    except ImportError:
        print("Warning: tweepy not available. Install with: pip install tweepy")
        return None

    try:
        # Initialize Twitter API client
        client = tweepy.Client(bearer_token=bearer_token)

        # Calculate date range
        if start_date and end_date:
            # Use provided range
            pass
        else:
            # Use days parameter
            end_date = datetime.now(timezone.utc)
            start_date = start_of_day(end_date - timedelta(days=days))

        # Get user by username
        user_response = client.get_user(
            username=username, user_fields=["public_metrics"]
        )
        if not user_response.data:
            print(f"Warning: Twitter user @{username} not found")
            return None

        user = user_response.data

        # Get recent tweets (Twitter API v2 free tier limits)
        tweets_response = client.get_users_tweets(
            id=user.id,
            start_time=start_date.isoformat(),
            end_time=end_date.isoformat(),
            tweet_fields=["created_at", "public_metrics"],
            max_results=100,  # API limit
        )

        tweets = tweets_response.data if tweets_response.data else []

        # Calculate stats
        total_tweets = len(tweets)
        total_likes = sum(t.public_metrics["like_count"] for t in tweets)
        total_retweets = sum(t.public_metrics["retweet_count"] for t in tweets)
        total_replies = sum(t.public_metrics["reply_count"] for t in tweets)

        return {
            "username": username,
            "total_tweets": total_tweets,
            "total_likes": total_likes,
            "total_retweets": total_retweets,
            "total_replies": total_replies,
            "tweets": tweets,
            "user_metrics": user.public_metrics,
        }

    except Exception as e:
        print(f"Warning: Failed to fetch Twitter data: {e}")
        return None


def get_aw_activity(
    days: int = 7,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    """Get ActivityWatch activity data for a date range.

    Args:
        days: Number of days to look back (default 7, used if start_date/end_date not provided)
        start_date: Optional start date (UTC)
        end_date: Optional end date (UTC)
    """
    try:
        from aw_client import ActivityWatchClient
    except ImportError:
        print("Warning: aw-client not available. Install with: pip install aw-client")
        return None

    try:
        # Connect to ActivityWatch
        aw = ActivityWatchClient("whatdidyougetdone", testing=False)

        # Calculate date range
        if start_date and end_date:
            # Use provided date range
            pass
        else:
            # Use days parameter
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


def get_user_activity(
    username: str,
    days: int = 7,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    """Get GitHub activity for a user over a date range.

    Args:
        username: GitHub username
        days: Number of days to look back (default 7, used if start_date/end_date not provided)
        start_date: Optional start date (UTC)
        end_date: Optional end date (UTC)
    """
    g = Github(os.getenv("GITHUB_TOKEN"))
    user = g.get_user(username)

    # Calculate date range (in UTC)
    if start_date and end_date:
        # Use provided date range
        pass
    else:
        # Use days parameter
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
                pr_ref = event.payload.get("pull_request", {})
                pr_number = pr_ref.get("number")

                # Fetch full PR details to get title, state, etc.
                # The event payload only contains PR reference, not full data
                try:
                    repo = g.get_repo(event.repo.full_name)
                    pr = repo.get_pull(pr_number)

                    state = pr.state
                    if pr.merged:
                        state = "merged"

                    activities.append(
                        {
                            "type": "pr",
                            "repo": event.repo.name,
                            "title": pr.title,
                            "state": state,
                            "number": pr.number,
                            "date": event.created_at,
                        }
                    )
                except Exception as e:
                    print(
                        f"Warning: Could not fetch PR #{pr_number} from {event.repo.name}: {e}"
                    )
                    # Fallback to incomplete data
                    activities.append(
                        {
                            "type": "pr",
                            "repo": event.repo.name,
                            "title": f"PR #{pr_number}",
                            "state": "unknown",
                            "number": pr_number,
                            "date": event.created_at,
                        }
                    )

    except Exception as e:
        print(f"Error fetching GitHub activity: {e}")

    return sorted(activities, key=lambda x: x["date"], reverse=True)


def generate_ai_summary(activities: list[dict], username: str, days: int) -> str:
    """Generate an AI-powered summary of user activity using gptme.

    Args:
        activities: List of activity dictionaries
        username: GitHub username
        days: Number of days covered

    Returns:
        AI-generated summary text
    """
    try:
        # Prepare activity summary for the LLM
        commit_count = sum(1 for a in activities if a["type"] == "commit")
        pr_count = sum(1 for a in activities if a["type"] == "pr")
        repos = {a["repo"] for a in activities}

        # Get sample commits and PRs
        commits = [
            a["message"].split("\n")[0] for a in activities if a["type"] == "commit"
        ][:10]
        prs = [a["title"] for a in activities if a["type"] == "pr"][:10]

        prompt = f"""Summarize this developer's activity over the past {days} days in 2-3 sentences.
Focus on key themes, types of work, and notable achievements.

Activity summary:
- {commit_count} commits across {len(repos)} repositories
- {pr_count} pull requests
- Repositories: {", ".join(list(repos)[:5])}
- Sample commits: {", ".join(commits[:5])}
- Sample PRs: {", ".join(prs[:5])}

Write a concise, engaging summary that highlights the developer's work. Be specific about types of changes (features, fixes, docs, etc.)."""

        # Call gptme to generate summary
        result = subprocess.run(
            ["gptme", "--non-interactive", prompt],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            summary = result.stdout.strip()
            # Remove any tool outputs or system messages, keep only the assistant response
            lines = summary.split("\n")
            # Skip lines that start with tool markers
            clean_lines = [
                line
                for line in lines
                if not line.startswith(("```", "System:", "User:"))
            ]
            summary = "\n".join(clean_lines).strip()
            return f"## 🤖 AI Summary\n\n{summary}\n\n"
        else:
            return f"⚠️ AI summary unavailable (gptme error: {result.stderr[:100]})\n\n"

    except subprocess.TimeoutExpired:
        return "⚠️ AI summary unavailable (gptme timeout)\n\n"
    except FileNotFoundError:
        return "⚠️ AI summary unavailable (gptme not installed)\n\n"
    except Exception as e:
        return f"⚠️ AI summary error: {str(e)}\n\n"


def generate_report(
    username: str,
    days: int = 7,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    include_timeline: bool = False,
    include_aw: bool = False,
    include_twitter: bool = False,
    ai_summary: bool = False,
):
    """Generate a markdown report of user activity.

    Args:
        username: GitHub username
        days: Number of days to look back (default 7, ignored if start_date/end_date provided)
        start_date: Optional start date (UTC)
        end_date: Optional end date (UTC)
        include_timeline: Include detailed timeline
        include_aw: Include ActivityWatch data
        include_twitter: Include Twitter/X activity data
        ai_summary: Include AI-generated summary
    """
    activities = get_user_activity(username, days, start_date, end_date)

    # Deduplicate PRs by URL (same PR can have multiple events)
    seen_prs = {}
    for activity in activities:
        if activity["type"] == "pr":
            # Use title + repo as key since URL might not always be present
            pr_key = f"{activity['repo']}:{activity['title']}"
            if pr_key not in seen_prs:
                seen_prs[pr_key] = activity

    # Calculate summary stats
    total_commits = sum(1 for a in activities if a["type"] == "commit")
    total_prs = len(seen_prs)  # Use deduplicated count
    active_repos = len({a["repo"] for a in activities})

    # Categorize PRs by type
    pr_categories: dict[str, list[dict]] = {
        "feat": [],
        "fix": [],
        "docs": [],
        "test": [],
        "chore": [],
        "other": [],
    }
    for pr_url, pr in seen_prs.items():
        title = pr["title"].lower()
        if title.startswith("feat"):
            pr_categories["feat"].append(pr)
        elif title.startswith("fix"):
            pr_categories["fix"].append(pr)
        elif title.startswith("docs"):
            pr_categories["docs"].append(pr)
        elif title.startswith("test"):
            pr_categories["test"].append(pr)
        elif title.startswith("chore") or title.startswith("refactor"):
            pr_categories["chore"].append(pr)
        else:
            pr_categories["other"].append(pr)

    # Generate markdown
    report = f"# What did {username} get done?\n\n"

    # Use custom date range in header if provided
    if start_date and end_date:
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")
        report += f"Activity from {start_str} to {end_str}:\n\n"
    else:
        report += f"Activity for the last {days} days:\n\n"

    # AI Summary
    if ai_summary:
        report += generate_ai_summary(activities, username, days)

    # Summary stats
    report += "## Summary\n\n"
    report += f"- 💻 {total_commits} commits\n"
    report += f"- 🔀 {total_prs} pull requests\n"
    report += f"- 📦 {active_repos} active repositories\n"

    # PR breakdown by category
    if total_prs > 0:
        report += "\n### PR Breakdown by Type\n\n"
        for category, prs in pr_categories.items():
            if prs:
                category_emoji = {
                    "feat": "✨",
                    "fix": "🐛",
                    "docs": "📝",
                    "test": "🧪",
                    "chore": "🔧",
                    "other": "📦",
                }
                emoji = category_emoji.get(category, "📦")
                report += f"- {emoji} {category.capitalize()}: {len(prs)}\n"

    # Add ActivityWatch data if available
    if include_aw:
        aw_data = get_aw_activity(days, start_date, end_date)
        if aw_data:
            report += f"- ⏱️ {aw_data['total_hours']:.1f} hours of local activity\n"

    # Add Twitter/X data if available
    if include_twitter:
        twitter_data = get_twitter_activity(username, days, start_date, end_date)
        if twitter_data:
            report += f"- 🐦 {twitter_data['total_tweets']} tweets\n"
            report += f"- ❤️ {twitter_data['total_likes']} likes received\n"
            report += f"- 🔄 {twitter_data['total_retweets']} retweets\n"

    report += "\n"

    # ActivityWatch section
    if include_aw:
        aw_data = get_aw_activity(days, start_date, end_date)
        if aw_data and aw_data["apps"]:
            report += "## Local Activity (via ActivityWatch)\n\n"
            report += "Top applications by time:\n\n"
            for app in aw_data["apps"]:
                app_name = app["data"].get("app", "Unknown")
                hours = app["duration"] / 3600
                report += f"- 💻 {app_name}: {hours:.1f}h\n"
            report += "\n"

    # Twitter/X section
    if include_twitter:
        twitter_data = get_twitter_activity(username, days, start_date, end_date)
        if twitter_data and twitter_data["tweets"]:
            report += "## Twitter/X Activity\n\n"
            report += f"Account: @{twitter_data['username']}\n\n"
            report += "### User Metrics\n\n"
            metrics = twitter_data["user_metrics"]
            report += f"- 👥 {metrics['followers_count']:,} followers\n"
            report += f"- 📝 {metrics['tweet_count']:,} total tweets\n"
            report += "\n### Recent Tweets\n\n"
            for tweet in twitter_data["tweets"][:10]:  # Show top 10
                date = tweet.created_at.strftime("%Y-%m-%d")
                likes = tweet.public_metrics["like_count"]
                retweets = tweet.public_metrics["retweet_count"]
                text = tweet.text[:100] + "..." if len(tweet.text) > 100 else tweet.text
                report += f"- 📅 {date} | ❤️ {likes} | 🔄 {retweets}\n"
                report += f"  {text}\n\n"

    # Group by repo using deduplicated PRs
    repos: dict[str, dict[str, list]] = {}

    # Add all commits
    for activity in activities:
        if activity["type"] == "commit":
            repo = activity["repo"]
            if repo not in repos:
                repos[repo] = {"commits": [], "prs": []}
            repos[repo]["commits"].append(activity)

    # Add deduplicated PRs
    for pr_key, pr in seen_prs.items():
        repo = pr["repo"]
        if repo not in repos:
            repos[repo] = {"commits": [], "prs": []}
        repos[repo]["prs"].append(pr)

    # Activity by repo
    report += "## Activity by Repository\n\n"
    for repo, acts in repos.items():
        report += f"### {repo}\n\n"

        # PRs with better formatting
        if acts["prs"]:
            for pr in sorted(acts["prs"], key=lambda x: x["date"], reverse=True):
                # State emoji
                state_emoji = {"merged": "✅", "open": "🔄", "closed": "❌"}.get(
                    pr["state"], "🔀"
                )

                # Format: emoji title (state)
                title = pr["title"]
                report += f"- {state_emoji} {title}\n"
            report += "\n"

        # Commits
        commits = acts["commits"]

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
@click.option(
    "--days",
    default=7,
    help="Number of days to look back (ignored if --start-date and --end-date provided)",
)
@click.option("--start-date", help="Start date (YYYY-MM-DD, requires --end-date)")
@click.option("--end-date", help="End date (YYYY-MM-DD, requires --end-date)")
@click.option("--file", help="Save output to file instead of stdout")
@click.option("--timeline", is_flag=True, help="Include detailed timeline")
@click.option("--activitywatch", is_flag=True, help="Include local ActivityWatch data")
@click.option("--twitter", is_flag=True, help="Include Twitter/X activity data")
@click.option(
    "--ai-summary", is_flag=True, help="Include AI-generated summary (uses gptme CLI)"
)
def report(
    username: str,
    days: int,
    start_date: Optional[str],
    end_date: Optional[str],
    file: Optional[str],
    timeline: bool,
    activitywatch: bool,
    twitter: bool,
    ai_summary: bool,
):
    """Generate activity report for a single user.

    Use --days for recent activity, or --start-date and --end-date for a specific range.
    """
    # Parse and validate date range
    parsed_start_date: Optional[datetime] = None
    parsed_end_date: Optional[datetime] = None

    if start_date or end_date:
        # Both must be provided if either is provided
        if not (start_date and end_date):
            click.echo(
                "Error: Both --start-date and --end-date must be provided together"
            )
            return

        try:
            # Parse dates and make them timezone-aware (UTC)
            parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
            parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, tzinfo=timezone.utc
            )

            # Validate date range
            if parsed_start_date >= parsed_end_date:
                click.echo("Error: --start-date must be before --end-date")
                return

        except ValueError as e:
            click.echo(f"Error parsing dates: {e}")
            click.echo("Date format should be YYYY-MM-DD (e.g., 2024-01-15)")
            return

    report_text = generate_report(
        username,
        days,
        start_date=parsed_start_date,
        end_date=parsed_end_date,
        include_timeline=timeline,
        include_aw=activitywatch,
        include_twitter=twitter,
        ai_summary=ai_summary,
    )

    if file:
        with open(file, "w") as f:
            f.write(report_text)
        print(f"Report saved to {file}")
    else:
        print(report_text)


@cli.command()
@click.argument("usernames", nargs=-1)
@click.option(
    "--days",
    default=7,
    help="Number of days to look back (ignored if --start-date and --end-date provided)",
)
@click.option("--start-date", help="Start date (YYYY-MM-DD, requires --end-date)")
@click.option("--end-date", help="End date (YYYY-MM-DD, requires --start-date)")
@click.option("--file", help="Save output to file instead of stdout")
@click.option("--timeline", is_flag=True, help="Include detailed timeline")
@click.option("--twitter", is_flag=True, help="Include Twitter/X activity data")
def team(
    usernames: tuple[str],
    days: int,
    start_date: Optional[str],
    end_date: Optional[str],
    file: Optional[str],
    timeline: bool,
    twitter: bool,
):
    """Generate combined activity report for multiple users"""
    if not usernames:
        print("Error: Please provide at least one username")
        return

    # Parse and validate date range
    parsed_start_date: Optional[datetime] = None
    parsed_end_date: Optional[datetime] = None

    if start_date or end_date:
        # Both must be provided if either is provided
        if not (start_date and end_date):
            click.echo(
                "Error: Both --start-date and --end-date must be provided together"
            )
            return

        try:
            # Parse dates and make them timezone-aware (UTC)
            parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
            parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, tzinfo=timezone.utc
            )

            # Validate date range
            if parsed_start_date >= parsed_end_date:
                click.echo("Error: --start-date must be before --end-date")
                return

        except ValueError as e:
            click.echo(f"Error parsing dates: {e}")
            click.echo("Date format should be YYYY-MM-DD (e.g., 2024-01-15)")
            return

    # Generate header with appropriate date range text
    report_text = "# Team Activity Report\n\n"
    if parsed_start_date and parsed_end_date:
        report_text += f"Activity from {start_date} to {end_date}:\n\n"
    else:
        report_text += f"Activity for the last {days} days:\n\n"

    for username in usernames:
        print(f"Fetching activity for {username}...")
        user_report = generate_report(
            username,
            days,
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            include_timeline=timeline,
            include_aw=False,
            include_twitter=twitter,
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
