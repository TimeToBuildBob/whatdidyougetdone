# What did TimeToBuildBob get done?

Activity for the last 7 days:

## Summary

- 💻 0 commits
- 🔀 29 pull requests
- 📦 4 active repositories

### PR Breakdown by Type

- ✨ Feat: 7
- 🐛 Fix: 19
- 📝 Docs: 1
- 🧪 Test: 1
- 🔧 Chore: 1

## Activity by Repository

### pi-skills

- 🔄 docs: add gptme installation instructions

### gptme

- ✅ fix(server): replace assertions with explicit error checks in production code
- ✅ fix(tools): graceful degradation for unavailable tools in server context
- 🔄 feat(eval): add practical7 suite — ini-to-json, json-diff, changelog-gen
- 🔄 fix: assorted bug fixes — wrong tool name, missing timeout, dead code, race guard
- 🔄 feat(eval): add practical6 suite — csv-analysis, word-frequency, merge-configs
- 🔄 fix(tokens): graceful fallback when tiktoken unavailable or offline
- 🔄 fix(models): update Claude 4.6 context window to 1M (GA)
- 🔄 fix(tests): replace pytest-mock mocker fixture with unittest.mock
- 🔄 fix(shell): preserve output when last line lacks trailing newline
- 🔄 fix(tests): mark test_python tests as slow to fix flaky CI
- 🔄 fix: replace bare except clauses and unclosed file handle
- 🔄 fix(types): resolve mypy errors in chats tool and gh tests
- ✅ fix(eval): close file handle in SWEBenchInfo.save_to_log_dir
- 🔄 fix(precommit): run checks on modified files only in TURN_POST hook
- ✅ fix(server): close TOCTOU race on acp_runtime in step request handler
- ✅ test(eval): add runtime guard and test for duplicate test names
- ✅ fix(server): guard acp_runtime None in _acp_step finally block

### gptme-contrib

- 🔄 fix(status): handle systemctl marker prefix in status-systemd.sh
- 🔄 feat(sessions): add ab_group and tier_version fields to SessionRecord
- ✅ fix(tests): isolate git config writes from host repo in test_git_hooks
- ✅ feat(dashboard): client-side search fallback for static gh-pages deployments
- ✅ fix(dashboard): include source attribution in search results for submodule lessons/skills
- ✅ feat(dashboard): add packages and plugins to search index
- ✅ feat(dashboard): show context_tier in sessions panel
- ✅ feat(sessions): add context_tier tracking to session records
- ✅ fix(dashboard): session fallback scan, search excerpt rendering, UX improvements

### agent-workspace-plugin

- ✅ chore: restore valid metadata fields in plugin.json
- ✅ fix: align plugin format with official Anthropic conventions

