# Team Activity Report

Activity for the last 7 days:

Activity for the last 7 days:

## Summary

- 💻 0 commits
- 🔀 13 pull requests
- 📦 7 active repositories

### PR Breakdown by Type

- ✨ Feat: 1
- 🐛 Fix: 7
- 📦 Other: 5

## Activity by Repository

### gptme-agent-template

- ❌ Random PR 25843

### gptme

- ❌ fix(acp): upgrade AvailableCommandsUpdate logging for slash command debugging
- ✅ fix(shell): don't use start_new_session in TTY path
- ❌ fix(webui): rename env vars to VITE_GPTME_ prefix convention
- ❌ fix: use VITE_GPTME_FLEET_BASE_URL as env var for base urls
- ✅ fix(shell): close leaked pipes via SESSION_END hook

### aw-webui

- ❌ fix(ci): handle missing server log files in cleanup steps
- ❌ feat(queries): add Helium browser support

### aw-tauri

- ❌ ci: windows arm build

### gptme-rag

- ❌ fix: fixed reindexing of unchanged files, now uses last_modified stamp

### activitywatch

- ❌ Replace aw-qt with aw-tauri

### superuserlabs.github.io

- ✅ Bold redesign: full dark theme, bento grid, visual hierarchy
- ✅ Modernize site design, new favicon, add Bob as team member


---

Activity for the last 7 days:

## Summary

- 💻 0 commits
- 🔀 49 pull requests
- 📦 8 active repositories

### PR Breakdown by Type

- ✨ Feat: 8
- 🐛 Fix: 30
- 📝 Docs: 1
- 🧪 Test: 1
- 🔧 Chore: 1
- 📦 Other: 8

## Activity by Repository

### gptme

- 🔄 test: skip test_url and test_vision for gpt-4o-mini
- 🔄 fix(acp): defer session-open notifications to after NewSessionResponse
- 🔄 fix(acp): return None from load_session to fix Zed session restore
- 🔄 feat(cli): add auto_envvar_prefix for GPTME_* env vars
- 🔄 feat(models): add per-model default tool_format to ModelMeta
- ✅ fix(acp): resend AvailableCommandsUpdate on first prompt() to fix Zed race condition
- ✅ fix(auth): don't truncate OAuth URL in fallback message
- ✅ fix(agent): replace template strings in gptme-agent create
- ❌ fix(acp): upgrade AvailableCommandsUpdate logging for slash command debugging
- ✅ fix(logmanager,tmux): prevent crashes on undo overflow and send-keys missing args
- ✅ fix(acp): include gptme version in ACP agent startup log
- ✅ feat(acp): send AvailableCommandsUpdate on session start
- ✅ fix(acp): replace assert guards with explicit runtime checks
- ✅ fix(todo): allow setting paused state on todo items
- ✅ style: enable PT011/PT022 rules, clean up unused noqa and imports
- ✅ style: enable FLY, ISC, PLE, PERF ruff rules
- ✅ fix(models): update Anthropic model metadata per official docs
- ✅ style: enable TCH, PIE810, PT003/PT006/PT022 ruff rules
- ✅ feat(acp): send model and workspace info on session open
- ✅ fix: duplicate name entry, explicit encoding, simplified exception
- ✅ style: remove self-assignment and add timezone to datetime.now() calls
- ✅ fix(acp): guard session_update calls against null connection in prompt()
- ✅ fix(context): use proper type annotations in config dataclasses
- ✅ refactor(acp): remove unused adapter scaffolding
- ✅ style: add explicit check param to subprocess.run() calls (PLW1510)

### gptme-agent-template

- 🔄 fix: prevent fork.sh from replacing CLI tool references with agent name
- ✅ feat: modular forking with --minimal, --without-*, and --with-* flags

### activitywatch

- ❌ feat: replace aw-notify (Python) with aw-notify-rs (Rust)
- ✅ feat: add aw-tauri CI builds alongside aw-qt

### gptme-contrib

- ✅ feat(run-loops): add --model and --tool-format options to autonomous command
- ✅ fix(lessons): add duplicate comment prevention to github-issue-engagement
- ✅ fix: enable cross-package pytest and modernize annotations

### aw-webui

- 🔄 fix(ci): handle missing server log files in cleanup steps
- ✅ fix(timeline): truncate long synced bucket names in sidebar
- ✅ fix(timeline): position tooltip above cursor to prevent overlap
- ✅ fix: allow single-date selection in timeline date range picker
- ✅ fix: pass bucket ID correctly for event editing in timeline views
- ✅ fix(sunburst-clock): respect startOfDay offset when rendering the clock
- ✅ docs: add --webpath instructions for aw-server-rust
- ✅ fix: support file exports in Tauri webview
- ✅ fix(settings): prevent categorization crash when hostname not yet resolved

### aw-tauri

- 🔄 ci(build): add Windows ARM64 to build workflow
- ✅ ci: add Windows ARM64 build support in release workflow

### aw-server-rust

- ✅ ci(lint): switch clippy from nightly to stable toolchain
- ✅ fix(dirs): restore /log subdirectory in log path after appdirs migration
- ✅ fix: replace appdirs with dirs for Windows ARM64 compatibility

### gptme-rag

- ✅ fix: dead code, perf, type safety, safer I/O
- ✅ fix(watcher): implement document removal on file deletion
- ✅ fix: remove unused imports and fix type annotations


---

