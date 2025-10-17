# Weekly Report Template

Example command:
```bash
./whatdidyougetdone.py report <username> --days 7 --timeline
```

## Purpose
Comprehensive weekly activity overview with detailed timeline.

## Format
- Full week of contributions (7 days)
- Detailed timeline of activities
- PR breakdown by type (Feat, Fix, Test, etc.)
- Repository-grouped activity

## Example Output
```markdown
# What did @username get done this week?

## Summary
- 💻 15 commits across 5 repositories
- 🔀 8 pull requests
- 📦 5 active repositories

### PR Breakdown by Type
- ✨ Feat: 3 new features
- 🐛 Fix: 4 bug fixes
- 📝 Docs: 1 documentation update

## Activity by Repository

### ProjectA
- ✅ feat: implement new authentication flow
- ✅ fix: resolve race condition in cache
- 🔄 docs: update API documentation

### ProjectB
- ✅ fix: correct pagination logic
- 🔄 feat: add dark mode support
```

## Best Practices
- Generate every Friday for weekly review
- Use --timeline for detailed daily breakdown
- Share in team meetings
- Include --ai-summary for narrative format
- Save to file with --file for archival
