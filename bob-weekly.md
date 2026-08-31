# What did TimeToBuildBob get done?

Activity for the last 7 days:

## Summary

- 💻 0 commits
- 🔀 36 pull requests
- 📦 7 active repositories

### PR Breakdown by Type

- ✨ Feat: 10
- 🐛 Fix: 23
- 📝 Docs: 2
- 📦 Other: 1

## Activity by Repository

### gptme-contrib

- ✅ fix(rag): handle large collection indexing failures
- 🔄 fix(gptme-sessions): close step_types LOO attribution gaps
- ✅ feat(gptme-sessions): add step_types field to SessionRecord for LOO attribution
- ✅ fix(vision-node): join capture thread before camera release
- ✅ feat(lesson_matcher): add match.repos repository gate
- ✅ fix(gptme-voice): preserve remote-party identity with open/closed call groups
- 🔄 fix(gptodo): retry once on transient 401 auth-death in spawn_agent
- ✅ fix(pm): stop treating AI-reviewer output as PM's own activity
- ✅ feat(voice): bridge BobBrain vision into live calls
- ✅ fix(activity-gate): treat round-capped P2-only reviews as clean
- ✅ fix(browser-semantic): label benchmark as static proxy
- ✅ feat(voice): capability-gated body_* tools — BodyAdapter + MAVSDK/PX4 support
- ✅ fix(activity-summary): recover malformed gptme summary JSON
- ✅ fix(gptme-activity-summary): isolate nested gptme logs from parent session
- ✅ fix(gptme-activity-summary): strip think tags + raw_decode JSON in gptme fallback
- ✅ feat(dotfiles): add Git-Session-Id prepare-commit-msg hook
- ✅ fix(news): parse total stars when GitHub wraps the count in an octicon

### aw-webui

- 🔄 fix(query): use native date inputs in query options
- 🔄 feat(categories): support field-scoped regex rules on master

### gptme

- 🔄 feat(context): add context-scout pre-pass (cheap model identifies relevant files)
- 🔄 fix(knowledge): don't block on gptme-rag index after save/delete
- 🔄 docs: add core domain guide
- 🔄 fix(webui): disable task creation in offline demo mode
- ✅ fix(llm): stop double-retrying and survive 429s in interactive mode
- ✅ fix(util): handle embedded nulls in batch prompts
- ✅ feat(knowledge): inject matching KB entries at session start
- ✅ fix(webui): gate task creation in demo mode
- 🔄 fix(shell): require confirmation for git-credentials and gptme config.toml reads
- 🔄 fix(browser): gate PDF fetches with the shared URL helper
- ❌ fix(security): enforce safe URL scheme validation in browser PDF fetcher (#3643)

### aw-server

- ✅ feat(profile): add --profile flag and port/settings isolation

### aw-android

- ✅ ci: fail closed if a pre-release tag would publish to Play production
- 🔄 fix(notify): accept canonical shared config schema

### gptme-agent-template

- ✅ docs(tasks): document gptodo ready --skip-claimed for concurrent sessions
- ✅ fix(precommit): scope task frontmatter validation

### aw-server-rust

- 🔄 feat(privacy-filter): capture-group replacement in redact

