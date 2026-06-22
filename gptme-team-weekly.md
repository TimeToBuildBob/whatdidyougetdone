# Team Activity Report

Activity for the last 7 days:

Activity for the last 7 days:

## Summary

- 💻 0 commits
- 🔀 4 pull requests
- 📦 3 active repositories

### PR Breakdown by Type

- 📦 Other: 4

## Activity by Repository

### gptme

- 🔄 [codex] fix webui rerun tool session id
- ✅ build(deps): bump the python-minor-patch group with 31 updates

### gptme-contrib

- ✅ [codex] add reusable autonomous session gate

### gptme-agent-template

- 🔄 [codex] add opt-in session gate for autonomous runners


---

Activity for the last 7 days:

## Summary

- 💻 0 commits
- 🔀 46 pull requests
- 📦 4 active repositories

### PR Breakdown by Type

- ✨ Feat: 12
- 🐛 Fix: 29
- 📝 Docs: 1
- 🧪 Test: 2
- 🔧 Chore: 1
- 📦 Other: 1

## Activity by Repository

### gptme

- ✅ feat(subagent): add subagent_list() tool for observability
- ✅ feat(logmanager): append-only event log for session durability (Phase 1)
- ✅ feat(server): add /api/v2/version endpoint
- ✅ fix(config): tolerate PermissionError in ChatConfig.from_logdir workspace mkdir
- ✅ docs(config): add model selection guide and provider-key reference
- ✅ fix(tests): mock thread creation in test_subagent_status_returns_dict
- ✅ feat(server): add API version constants, contract_revision, and X-API-Version header
- ✅ fix(cli): make tokens count --file - read from stdin
- ✅ fix(server): prevent external-sessions endpoint from hanging on large session catalogs
- ✅ feat(subagent): add redact_secrets option for context isolation
- ✅ fix(tools): normalize bare callables in ToolSpec.functions (server won't start with plugins)
- ✅ feat(webui): chat UI polish — role-aligned message footer + Chat-button sidebar toggle
- ✅ fix(webui): code-block rendering improvements + emoji additions + star move
- ✅ feat(cli): add gptme-resume subcommand for lossy session rehydration
- ✅ fix(cli): validate model provider early, before context_cmd runs
- ✅ feat(cli): add `gptme-util snapshot list` subcommand
- ✅ fix(server): preserve 'files' field in PUT /api/v2/conversations/:id messages
- ✅ test(server): perf gate for GET /api/v2/conversations with 100 conversations
- ✅ fix(server): enforce workspace containment at config PUT/PATCH boundary
- ❌ fix(server): prevent workspace path traversal via config PATCH and PUT
- ✅ fix(test): use json.dumps for valid JSON in kimi_k2 test
- ✅ fix(webui): extract ConversationItem to module level
- ✅ perf(server): partial cache update on message POST to avoid O(N) rescan
- ✅ fix(server): accept --tools none to disable all tools
- ✅ chore(deps): group dependabot minor/patch bumps into single PRs
- ✅ feat(webui): fork conversations from any message
- ✅ fix(webui): avoid sidebar log scans

### gptme-contrib

- ✅ fix(perplexity): use current sonar model; extract citations
- ✅ fix(tests): remove spurious @patch decorator leaking MagicMock/ to workspace root
- ✅ fix(evolution): mkdir parents before saving history/refinements with slashed lesson IDs
- ✅ fix(lessons): remove 20 dead keywords from 5 active lessons
- ✅ fix(lessons): remove 8 dead keywords from 4 active lessons
- ✅ fix(pm): per-check slot key for concurrent master-CI failures
- ✅ fix(gptmail): agent read command now marks message read
- ✅ fix(gptmail): stamp read: true on pull-fetched msgs with no read: key
- ✅ fix(match-lessons): skip node_modules and tool dirs during lesson scan
- ✅ fix(match-lessons): default harness to 'gptme' when no env vars set
- ✅ fix(lessons): restore hook skill routing metadata
- ✅ fix(pm-bandit): add fcntl locking to record_outcome to prevent lost updates
- ✅ feat(gptodo): auto-set waiting_since when transitioning to waiting state
- ✅ fix(gptme-usage): mark Agent SDK credit change as paused
- ✅ test(gptme-usage): add coverage for resolve_cc_version and is_post_agent_sdk_credit_change
- ✅ feat(subscription): add live token-probe script with refresh-aware stale-slot detection

### activitywatch

- ✅ fix(ci): pin GitHub Actions to commit SHAs (supply chain hardening)
- ✅ fix(deps): unblock pip security updates

### sessionwiki

- ❌ feat(adapters): add gptme adapter


---

