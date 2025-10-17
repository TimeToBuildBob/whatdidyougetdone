# Custom Format Template

## Advanced Options

### Date Range Report
```bash
./whatdidyougetdone.py report <username> \
  --start-date 2025-01-01 \
  --end-date 2025-01-31
```
Generate report for specific date range (e.g., monthly reports).

### Timeline View
```bash
./whatdidyougetdone.py report <username> --days 7 --timeline
```
Include detailed daily timeline of activities.

### ActivityWatch Integration
```bash
./whatdidyougetdone.py report <username> --days 7 --activitywatch
```
Combine GitHub activity with local ActivityWatch data for comprehensive view.

### AI-Generated Summary
```bash
./whatdidyougetdone.py report <username> --days 7 --ai-summary
```
Generate natural language summary using gptme CLI.

### Combined Options
```bash
./whatdidyougetdone.py report <username> \
  --days 7 \
  --timeline \
  --activitywatch \
  --ai-summary \
  --file weekly-report.md
```
Full-featured report with all enhancements saved to file.

## Custom Use Cases

### Sprint Review Report
```bash
# 2-week sprint report
./whatdidyougetdone.py report <username> --days 14 --timeline
```

### Monthly Summary
```bash
# First day to last day of month
./whatdidyougetdone.py report <username> \
  --start-date 2025-01-01 \
  --end-date 2025-01-31 \
  --ai-summary
```

### Team Sprint Report
```bash
# Combined team sprint report
./whatdidyougetdone.py team user1 user2 user3 \
  --days 14 \
  --file sprint-report.md
```

### Shareable Weekly Update
```bash
# Professional weekly update for social media
./whatdidyougetdone.py report <username> \
  --days 7 \
  --ai-summary \
  --file weekly-update.md
```

## Format Customization Tips

1. **Concise Format**: Use basic command without --timeline
2. **Detailed Format**: Add --timeline for daily breakdown
3. **Professional Format**: Add --ai-summary for polished narrative
4. **Complete Format**: Combine with --activitywatch for full picture
5. **Archival Format**: Always use --file to save reports

## Best Practices

- Choose format based on audience (team, manager, public)
- Use date ranges for consistent reporting periods
- Save important reports with --file for archival
- Experiment with combinations to find your style
- Use AI summaries for external sharing
