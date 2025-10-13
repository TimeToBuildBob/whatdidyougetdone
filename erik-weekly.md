# What did ErikBjare get done?

Activity report for the last 7 days:

## Summary

- 💻 46 commits
- 🔀 7 pull requests
- 📦 2 active repositories

## Activity by Repository

### gptme/gptme-webui

- 💻 docs: improved the usage instructions, mention gptme.ai
### gptme/gptme

- 🔀 Fix: Pin openai version in pre-commit mypy config (closed)
- 🔀 feat(browser): add Accept header to prefer markdown/plaintext (closed)
- 🔀 feat(telemetry): add hostname to resource attributes (closed)
- 🔀 feat(telemetry): add agent name and interactive mode metadata (closed)
- 🔀 fix(telemetry): switch to using OTLP for both metrics and traces (closed)
- 🔀 fix: improved prompting for complete tool (closed)
- 🔀 fix: improved prompting for complete tool (open)
- 💻 docs: improve server docs, mention gptme.ai
- 💻 fix: show full path in patch tool output
- 💻 refactor(mcp): consolidate info/discover commands into smart info command
- 💻 fix(mcp): implement correct registry API endpoints
- 💻 feat(mcp): add discovery commands to gptme-util CLI
- 💻 fix(anthropic): set temperature/top_p only for models not supporting reasoning, even if thinking disabled (as if due to --tool-format tool)
- 💻 fix: remove emoji from OTLP log message
- 💻 fix: remove redundant log message
- 💻 feat: add tool_format to telemetry and remove redundant log
- 💻 fix: shortened telemetry startup log
- 💻 fix(ci): pin openai version in pre-commit mypy config (#682)
- 💻 feat(browser): add Accept header to prefer markdown/plaintext over HTML (#680)
- 💻 feat(telemetry): add hostname to resource attributes (#676)
- 💻 feat(telemetry): add agent name and interactive mode metadata (#675)
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
