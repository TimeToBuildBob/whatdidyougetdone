# Team Activity Report

Activity for the last 7 days:

Activity for the last 7 days:

## Summary

- 💻 0 commits
- 🔀 29 pull requests
- 📦 6 active repositories

### PR Breakdown by Type

- ✨ Feat: 9
- 🐛 Fix: 6
- 🔧 Chore: 6
- 📦 Other: 8

## Activity by Repository

### activitywatch.github.io

- ✅ stats: add Android rating + crash-rate charts
- ✅ feat: show newer pre-release on downloads page (robust, from real assets)
- ✅ chore: bump checkout->v5, setup-python->v6 (Node 24 native)
- ✅ chore: bump checkout@v2->v4 and setup-python@v1->v5
- ✅ stats: self-host stargazers chart (fix broken starchart.cc embed)
- ✅ stats: show downloads chart per-week instead of per-day

### aw-android

- ❌ feat: multi-browser web watcher via Accessibility Service
- ❌ fix: attempt at fixing CSV exports crashing app
- ✅ fix(ci): add rubygems.org source before fastlane release step

### stats

- ✅ chore: raise minimum Python to 3.10
- ✅ feat: chart loaders for Android crash-rate + rating
- ✅ ci: add ruff + mypy + pytest
- ✅ feat: collect Android Play Store rating history
- ✅ feat: switch installed.csv to Active Device Installs + automate in CI
- ✅ fix(ci): hold installs update pending metric decision
- ✅ feat(vitals): add 'errors' command (crash/ANR clusters + stacktraces)
- ✅ feat: Play Console collectors — Android vitals (crash/ANR) + installs automation
- ✅ chore: refresh android installed.csv through 2026-07-07
- ✅ fix: smooth per-day rate chart + honest label (unbreak jagged downloads.png)
- ✅ fix: restore poetry package-mode=false (unbreak activitywatch.github.io build)
- ✅ improve stats collection: incremental releases + per-asset download tracking
- ✅ chore: refresh firefox/chrome stats, switch to uv

### gptme

- ✅ chore(deps): bump rich to 14.x and textual to 8.x
- ✅ feat(cli): compact log output for user-facing CLIs
- ✅ perf: cut startup time ~6x by deferring heavy imports
- 🔄 build(deps): bump the python-minor-patch group across 1 directory with 6 updates
- ✅ feat(tui): add Textual-based TUI (gptme-tui)

### gptme-contrib

- ✅ perf(gptme-tts): lazy-import scipy/numpy/requests

### aw-server-rust

- ❌ fix: update aw-webui submodule to valid upstream commit (64ed7a7)


---

Activity for the last 7 days:

## Summary

- 💻 0 commits
- 🔀 23 pull requests
- 📦 6 active repositories

### PR Breakdown by Type

- ✨ Feat: 9
- 🐛 Fix: 13
- 🔧 Chore: 1

## Activity by Repository

### gptme

- 🔄 feat(prompts): add brief response mode
- ✅ fix(computer): capture pre-action baseline on native xdotool path in act_and_observe
- ✅ fix: resolve cache_tokens test failures for openai 2.45.0 and acp 0.11.0
- ✅ fix(ci): add overwrite: true to tauri release artifact uploads
- 🔄 fix(deps): update code for acp 0.11.0 and openai 2.45.0 breaking changes
- ❌ chore(ci): fix nonexistent GitHub Actions versions across all workflows
- ✅ fix(tauri): sync webui to managed server port
- 🔄 feat(subagent): add max_concurrent fleet cap to subagent_parallel()
- ✅ feat(subagent): add SubagentBudget for fleet-wide token budget coordination
- ✅ feat(tauri): add GPTME_SERVER_PORT env var to override default port
- ✅ feat(gptme-util): add `chats fork` for point-in-time session forking
- ✅ feat(context): proactive context-window summarization before hard limit

### aw-android

- 🔄 fix: remove FOREGROUND_SERVICE_DATA_SYNC permission (unblocks v0.14.0 Play Store upload)
- ❌ fix(hostname): use Build.DEVICE instead of Settings.Global.DEVICE_NAME
- ✅ feat(watcher): multi-browser WebWatcher with Firefox Compose toolbar support
- ✅ fix: CSV/JSON export via WebAppInterface + FileProvider (fixes #104)
- ✅ feat(sync): disable automatic sync by default
- ✅ fix: use Build.DEVICE instead of Build.MODEL for hostname fallback

### aw-server-rust

- ✅ fix(sync): chunk event fetch in sync_one() to prevent OOM on large buckets

### aw-webui

- ✅ fix(buckets): show phone icon for Android devices in Raw Data view
- ✅ fix(activity): detect Android device at runtime for view selection

### stats

- ✅ fix(android_installs): restrict zero filtering to trailing tail only

### gptme-contrib

- ✅ feat(bobutils): add shared workspace utility package (stdlib-only)


---

