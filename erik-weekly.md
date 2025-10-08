# What did ErikBjare get done?

Activity report for the last 7 days:

## Summary

- 💻 56 commits
- 🔀 13 pull requests
- 📦 2 active repositories

## Activity by Repository

### gptme/gptme

- 🔀 fix(telemetry): switch to using OTLP for both metrics and traces (closed)
- 🔀 fix: improved prompting for complete tool (closed)
- 🔀 fix: improved prompting for complete tool (open)
- 🔀 refactor: consolidate auto-compact/precommit functionality into tools (closed)
- 🔀 feat: implement /compact and auto-compacting (closed)
- 🔀 feat: wip anthropic 1M context support (open)
- 🔀 feat: implement comprehensive hook system and command registration (#156) (closed)
- 🔀 docs(shell): move timeout config from agent instructions to module docstring (closed)
- 🔀 fix: filter out empty text blocks in Anthropic API to prevent cache_control errors (closed)
- 🔀 feat: auto-restore todo state when resuming conversations (closed)
- 🔀 fix: prevent premature code block closure during streaming with nested blocks (closed)
- 💻 feat: reintroduce OpenAI and Anthropic telemetry instrumentation
- 💻 fix(telemetry): Strip http:// prefix from OTLP endpoint for gRPC
- 💻 fix: Update telemetry wrapper to match new signature
- 💻 fix: Update telemetry wrapper to match new signature
- 💻 fix: Remove remaining unused code and fix linting issues
- 💻 refactor: Remove unused Prometheus HTTP server fallback code
- 💻 docs: Remove Pushgateway references and update for OTLP HTTP
- 💻 fix(telemetry): Add full paths to HTTP exporter endpoints
- 💻 fix(telemetry): Switch to HTTP exporters for better compatibility
- 💻 fix(complete): stop session immediately after complete tool
- 💻 fix(autocompact): handle Log objects in hook
- 💻 fix(complete): handle Log objects in complete_hook
- 💻 debug: add logging to complete_hook for diagnosis
- 💻 feat: add GENERATION_PRE hook trigger before LLM generation
- 💻 fix: use trigger_hook function to properly trigger hooks
- 💻 fix: pass workspace and manager args to GENERATION_PRE hooks
- 💻 fix(config): always apply CLI defaults for stream and interactive
- 💻 Revert "fix(config): always apply CLI defaults for stream and interactive"
- 💻 docs: comprehensive streaming bug investigation report
- 💻 fix(telemetry): support multiple CLI instances with automatic port selection
- 💻 docs: Add telemetry solutions document for multiple instances
- 💻 docs: Add Pushgateway setup guide
- 💻 docs: Add quick Pushgateway setup steps for server3
- 💻 feat: Complete Pushgateway setup and configuration
- 💻 docs: Clean up PR and update telemetry documentation
- 💻 feat: Add native Pushgateway support for telemetry
- 💻 refactor: consolidate auto-compact/precommit functionality into tools (#666)
- 💻 feat: implement comprehensive hook system and command registration (#156) (#660)
- 💻 docs(shell): move timeout config from agent instructions to module docstring (#662)
- 💻 fix: prevent cache_control on empty text blocks in Anthropic API (#653)
- 💻 fix: handle nested code blocks in patch blocks correctly
- 💻 test: add comprehensive nested codeblock tests
- 💻 test: document actual behavior of ambiguous bare backticks
- 💻 feat: emit hint when save tool barely changes file
- 💻 fix: add version header and correct heading levels in release notes
- 💻 refactor: simplify version header logic in build_changelog.py
- 💻 chore: remove build_changelog.py, now available upstream
- 💻 docs: fixed changelog index
- 💻 chore: improve changelog version detection and update contributors
- 💻 build: automatically update docs/changelog.rst in release target
- 💻 chore: bump version to 0.28.3
- 💻 fix: update CI anthropic model to claude-3-5-haiku
- 💻 fix(shell): denylist should not trigger on content in quoted strings or heredocs
- 💻 fix(shell): improve denylist patterns for git commands
- 💻 feat: add git safety guards to shell tool
- 💻 feat: improve save tool feedback with detailed status
### ActivityWatch/activitywatch

- 🔀 build: add --add-version-header flag to build_changelog.py (closed)
- 🔀 feat: add --add-version-header flag to build_changelog.py (open)
- 💻 build: add --add-version-header flag to build_changelog.py (#1179)
