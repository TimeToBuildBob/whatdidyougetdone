# What Did You Get Done? - Report Templates

This directory contains example templates and configurations for generating different types of activity reports.

## Available Templates

### 1. Daily Summary ([daily-summary-example.md](./daily-summary-example.md))
- **Purpose**: Quick daily overview
- **Use case**: Daily standups, end-of-day reviews
- **Duration**: 1 day
- **Format**: Concise, focused

### 2. Weekly Report ([weekly-report-example.md](./weekly-report-example.md))
- **Purpose**: Comprehensive weekly activity
- **Use case**: Weekly reviews, team updates
- **Duration**: 7 days
- **Format**: Detailed with timeline and PR breakdown

### 3. Team Overview ([team-overview-example.md](./team-overview-example.md))
- **Purpose**: Aggregate team activity
- **Use case**: Sprint reviews, management reports
- **Duration**: Flexible (typically 7-14 days)
- **Format**: Multi-user with individual breakdowns

### 4. Custom Formats ([custom-format-example.md](./custom-format-example.md))
- **Purpose**: Advanced options and combinations
- **Use case**: Specialized reports
- **Duration**: Custom date ranges
- **Format**: Highly configurable

## Quick Start

### Generate a Daily Summary
```bash
cd .. && ./whatdidyougetdone.py report <username> --days 1
```

### Generate a Weekly Report
```bash
cd .. && ./whatdidyougetdone.py report <username> --days 7 --timeline
```

### Generate a Team Report
```bash
cd .. && ./whatdidyougetdone.py team user1 user2 user3 --days 7
```

## Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `--days N` | Look back N days | `--days 7` |
| `--start-date` | Start date (YYYY-MM-DD) | `--start-date 2025-01-01` |
| `--end-date` | End date (YYYY-MM-DD) | `--end-date 2025-01-31` |
| `--timeline` | Include detailed timeline | `--timeline` |
| `--activitywatch` | Include local ActivityWatch data | `--activitywatch` |
| `--ai-summary` | Generate AI summary (requires gptme) | `--ai-summary` |
| `--file` | Save to file | `--file report.md` |

## Template Selection Guide

Choose your template based on:

1. **Frequency**: How often you report
   - Daily → Daily Summary
   - Weekly → Weekly Report
   - Sprint/Monthly → Custom Format

2. **Audience**: Who will read it
   - Self → Any format
   - Team → Weekly Report or Team Overview
   - Manager → Weekly Report with --ai-summary
   - Public → Custom Format with --ai-summary

3. **Detail Level**: How much information needed
   - High-level → Daily Summary
   - Moderate → Weekly Report
   - Detailed → Weekly Report with --timeline
   - Comprehensive → Custom Format with all options

## Best Practices

1. **Consistency**: Use the same format regularly for trend tracking
2. **Archival**: Always save important reports with --file
3. **Context**: Add AI summaries for external sharing
4. **Privacy**: Be mindful of what you share publicly
5. **Timing**: Generate reports at consistent intervals

## Examples in Action

### Personal Productivity Tracking
```bash
# Every Friday
./whatdidyougetdone.py report myusername --days 7 --file weekly/2025-01-17.md
```

### Team Sprint Review
```bash
# Every 2 weeks
./whatdidyougetdone.py team alice bob charlie --days 14 --file sprints/sprint-23.md
```

### Monthly Professional Update
```bash
# First of each month
./whatdidyougetdone.py report myusername \
  --start-date 2025-01-01 \
  --end-date 2025-01-31 \
  --ai-summary \
  --file monthly/2025-01.md
```

## Contributing

Have a useful template or format? Feel free to:
1. Create a new example file
2. Document the use case and commands
3. Submit a PR with your addition

## Related

- [Main README](../README.md) - Full project documentation
- [TEAM_DASHBOARD_MVP.md](../TEAM_DASHBOARD_MVP.md) - Web UI documentation
