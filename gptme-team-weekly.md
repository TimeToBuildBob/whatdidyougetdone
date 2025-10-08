# Team Activity Report

Activity for the last 7 days

## Team Summary

- 👥 2 team members
- 💻 130 commits
- 🔀 20 pull requests
- 📦 3 active repositories

## ErikBjare

- 💻 56 commits
- 🔀 13 pull requests
- 📦 2 active repositories

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

## TimeToBuildBob

- 💻 74 commits
- 🔀 7 pull requests
- 📦 2 active repositories

### gptme/gptme

- 🔀 fix(telemetry): Support multiple CLI instances with automatic port selection (open)
- 🔀 Consolidate auto-compact functionality into autocompact tool (open)
- 🔀 feat: add token budget awareness tool (open)
- 🔀 docs(shell): move timeout config from agent instructions to module docstring (open)
- 🔀 feat: implement comprehensive hook system and command registration (#156) (open)
- 🔀 feat: auto-restore todo state when resuming conversations (open)
- 🔀 fix: prevent premature code block closure during streaming with nested blocks (open)
- 💻 ci: added ci run for latest Python & package versions
- 💻 Revert "fix(config): always apply CLI defaults for stream and interactive"
- 💻 docs: comprehensive streaming bug investigation report
- 💻 fix(config): always apply CLI defaults for stream and interactive
- 💻 fix(autocompact): handle Log objects in hook
- 💻 fix(complete): handle Log objects in complete_hook
- 💻 debug: add logging to complete_hook for diagnosis
- 💻 feat: add GENERATION_PRE hook trigger before LLM generation
- 💻 fix: use trigger_hook function to properly trigger hooks
- 💻 fix: pass workspace and manager args to GENERATION_PRE hooks
- 💻 fix(complete): stop session immediately after complete tool
- 💻 feat: Implement OTLP metrics via OpenTelemetry Collector
- 💻 feat: Add native Pushgateway support for telemetry
- 💻 feat: add concise __repr__ to Log class
- 💻 refactor: consolidate auto-compact/precommit functionality into tools (#666)
- 💻 fix(telemetry): support multiple CLI instances with automatic port selection
- 💻 docs: Add telemetry solutions document for multiple instances
- 💻 docs: Add Pushgateway setup guide
- 💻 docs: Add quick Pushgateway setup steps for server3
- 💻 feat: Complete Pushgateway setup and configuration
- 💻 docs: Clean up PR and update telemetry documentation
- 💻 docs: Clean up PR and update telemetry documentation
- 💻 feat: Complete Pushgateway setup and configuration
- 💻 docs: Add quick Pushgateway setup steps for server3
- 💻 docs: Add Pushgateway setup guide
- 💻 docs: Add telemetry solutions document for multiple instances
- 💻 fix: fixed import in treeofthoughts script
- 💻 fix: prevent hook errors from stopping subsequent hooks
- 💻 feat: add concise __repr__ to Log class
- 💻 refactor: consolidate precommit and autocommit functions into tool files
- 💻 feat: implement auto-reply mechanism as LOOP_CONTINUE hook
- 💻 fix: prevent infinite loop when hooks fail
- 💻 fix: update todo test for new summary format
- 💻 fix: prevent autocompact infinite loop
- 💻 fix: reduce verbosity in hook error logging
- 💻 fix: adjust test to create content with proper token count
- 💻 fix(shell): prevent editors from breaking terminal state
- 💻 fix(api): support auto-generating agent path from name (#646)
- 💻 feat: add denylist for dangerous shell commands with specific deny reasons (#648)
- 💻 chore: bump version to 0.28.1
- 💻 chore: updated changelog_contributors.csv cache
- 💻 build: fix make release target
- 💻 docs: added release notes for v0.28.1
- 💻 docs: added release notes to index
- 💻 fix: improvements to evals/dspy/gepa (#652)
- 💻 fix: make num_trials parameter actually control DSPy optimizers and add CLI options for dataset sizes
- 💻 refactor: split GEPA into separate optimize-gepa subcommand with proper budget configuration
- 💻 feat: add dedicated gptme-dspy command entry point
- 💻 feat: add dry-run mode for DSPy optimization commands
- 💻 fix(llm): respect LLM_PROXY_URL for OpenRouter models endpoint
- 💻 fix: fixes to proxy openrouter support
- 💻 fix: add support for sonnet 4.5
- 💻 chore: bump version to 0.28.2
- 💻 docs: added release notes for v0.28.2
- 💻 docs: improve chat history prompt format
- 💻 docs: add intersphinx support for Python stdlib references
- 💻 fix: use double backslashes in docstrings to avoid Python syntax warnings
- 💻 docs: fix RST formatting in hooks.py docstrings
- 💻 docs: move command registration from hooks to custom tools
- 💻 docs: remove development documentation files
- 💻 fix: resolve CI test failures in hook system PR
- 💻 feat: add hook propagation stopping mechanism
- 💻 refactor: address TODOs - merge todo_replay and fix precommit auto-enable
- 💻 fix: improved complete tool detection in chat loop
- 💻 fix: increase number of past conversation summaries in system prompt to 5
- 💻 feat: implement complete tool and auto-reply mechanism for autonomous operation

### TimeToBuildBob/ai-adoption-score

- 💻 fix: only create Supabase client when needed
- 💻 feat: make Supabase integration optional
- 💻 feat: persist quiz results in localStorage
- 💻 docs: replace Vercel deployment with Cloudflare Pages and GitHub Pages options
- 💻 fix: resolve all TypeScript and ESLint errors
- 💻 feat: add Supabase backend integration

