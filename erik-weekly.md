# What did ErikBjare get done?

Activity for the last 7 days:

## Summary

- 💻 0 commits
- 🔀 20 pull requests
- 📦 10 active repositories

### PR Breakdown by Type

- ✨ Feat: 6
- 🐛 Fix: 7
- 🧪 Test: 3
- 📦 Other: 4

## Activity by Repository

### gptme

- 🔄 feat(tui): collapse long pastes into atomic placeholder tokens
- 🔄 feat(tui): --resume [NAME] — pick from a list, or open NAME directly
- 🔄 fix(tui): inline-mode UX — hide thinking by default, keep scrollback on resize, show queued prompts and confirm keys

### aw-server

- ✅ feat(query): cache results for finished past periods

### aw-core

- ✅ perf(query): cache parsed statements and category rules across queries

### aw-research

- ✅ perf(classify): match each distinct (title, app, url) once
- ✅ fix(classify): skip null title/app/url instead of raising

### gptme-contrib

- ✅ feat(runloops): one-shot resumable runs across backends (run_once + `run` CLI, codex executor)

### aw-webui

- ✅ feat(activity): choose all devices or a subset of devices in the Activity view
- ✅ test: tighten review follow-ups from #1001 and #1003

### aw-client

- ✅ feat(queries): add multidevice canonical query and host discovery

### aw-server-rust

- ✅ fix(aw-sync): read v4/v5 peer databases instead of skipping them

### quantifiedme

- ✅ fix(ci): read aw-server-rust logs from the testing profile's log dir
- ✅ build: require Python 3.12, bump aw-research
- ✅ fix(cache): key screentime and joblib caches on the content they depend on
- ❌ fix(ci): tolerate missing aw-server-rust logs in Echo logs step

### activitywatch

- ✅ build(deps): bump aw-core and aw-server-rust for the parity fixes
- ✅ test(query-parity): attribute known failures to their measured causes
- 🔄 test(query-parity): assert the startup poll actually retried
- ✅ fix(query-parity): retry startup polls on read timeouts, keep skipped cases' known failures

