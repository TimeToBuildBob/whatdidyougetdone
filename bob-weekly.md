# What did TimeToBuildBob get done?

Activity for the last 7 days:

## Summary

- 💻 0 commits
- 🔀 33 pull requests
- 📦 4 active repositories

### PR Breakdown by Type

- ✨ Feat: 13
- 🐛 Fix: 19
- 📦 Other: 1

## Activity by Repository

### gptme

- 🔄 feat(webui): toggleable external sessions in conversation list
- 🔄 feat(tools): make lxml optional with stdlib xml.etree fallback; move pypdf to optional
- 🔄 feat(packaging): add gptme[minimal] install extra for ARM/musl/Termux/Lambda
- 🔄 fix(tauri): make AppImage GTK links idempotent
- 🔄 feat(safety): add optional haiku judge annotation to export CLI
- ✅ experiment(computer): semantic verification contract prototype
- ✅ fix(acp): advertise authMethods in initialize response for ACP registry
- ✅ fix(llm): capture usage tokens from subscription response.done events
- ✅ fix(test): kill the leaked-thread teardown race class (moving "dictionary changed size during iteration" flake)
- ✅ fix(security): replace last bare 'git' subprocess call in tasks_api with GIT_CMD
- ✅ feat(webui): warn on server API incompatibility
- ✅ feat(context): expose initial prompt to context_cmd
- 🔄 feat(typecheck): add human-readable imprecision summary to typecheck-coverage
- ✅ fix(security): extend GIT_CMD hardening to all remaining bare git subprocess call sites
- ✅ fix(logmanager): don't merge adjacent tool-result system messages
- ✅ feat(webui): add BranchMapPanel to right sidebar
- ✅ fix(security): harden bare git subprocess resolution on native Windows
- ✅ fix(subagent): eliminate cancel status race — set result before writing control file
- ✅ feat(subagent): cooperative cancel checkpoint — make cancel actually stop thread-mode subagents
- ✅ feat(subagent): stop thread agents at control checkpoints
- ✅ fix(webui): latch demo mode so SPA URL rewrites can't split demo state
- ✅ fix(subagent): stop orphaned subagents at parent session end via SESSION_END hook

### gptme-contrib

- 🔄 fix(greptile-helper): mark trigger POST with BOB_GREPTILE_HELPER=1 sentinel
- ✅ fix(action-receipts): expose folder hook registration
- ✅ fix(runloops): serialize and atomically replace state writes
- ✅ fix(sessions): persist Codex cache-read tokens
- ✅ fix(sessions): use result message for CC stream-json token totals
- ✅ feat(wisdom): add prompt-aware context command
- 🔄 feat(security): gate outbound twitter and email content
- ✅ fix(twitter): quarantine current permanent reply error
- ✅ fix(agent-msg): accept explicit unread list flag

### registry

- 🔄 feat: add gptme agent

### harbor

- 🔄 fix(gptme): document container-safe tool allowlist

