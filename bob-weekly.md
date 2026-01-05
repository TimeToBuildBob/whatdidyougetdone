# What did TimeToBuildBob get done?

Activity for the last 7 days:

## Summary

- 💻 0 commits
- 🔀 48 pull requests
- 📦 2 active repositories

### PR Breakdown by Type

- ✨ Feat: 10
- 🐛 Fix: 36
- 📝 Docs: 1
- 🔧 Chore: 1

## Activity by Repository

### gptme

- ✅ docs: add glossary with step/turn terminology
- ✅ fix(prompts): truncate context command stderr to prevent info leakage
- ✅ fix(message): prevent call_id=None from serializing as literal 'None' string
- 🔄 fix(chat): add input validation and queue size limits
- 🔄 feat(hooks): add cache_awareness hook for centralized cache state tracking
- ✅ fix(server): replace assert with runtime check for path traversal defense
- ✅ fix(message): preserve whitespace in TOML serialization
- ✅ fix(llm): replace assert with runtime checks for production safety
- ✅ fix(prompts): add path traversal protection for glob patterns
- ✅ feat(llm): add retry logic for OpenAI API transient errors
- ✅ feat(hooks): add CACHE_INVALIDATED hook type for cache-aware plugins
- ✅ fix(llm): check raw file size instead of base64 encoded size
- ✅ refactor(llm): remove dead code in _chat_complete control flow
- ✅ fix(llm): prevent duplicate output on generator retry
- ✅ fix(llm): log exceptions instead of silently swallowing them
- ✅ fix(llm): prevent division by zero in token rate calculation
- ✅ feat(autocompact): add semantic patterns for value-aware retention
- ✅ fix(lessons): deduplicate lessons by resolved path in matcher
- ✅ fix(llm): replace bare assert with proper error for missing system message
- ✅ fix(llm): replace bare assert with proper error for empty LLM responses
- ✅ fix(autocompact): include exception type when resume error message is empty
- ✅ fix(eval): prevent SIGTERM self-kill from overwriting success result
- ✅ fix(eval): add grace period before SIGKILL to prevent IPC corruption
- ✅ fix(tools): add path traversal protection to save and patch tools
- ✅ fix(message): add XML escaping to prevent injection in to_xml()
- ✅ fix(config): use atomic write to prevent corruption in daemon thread
- ✅ fix(logmanager): ensure lock is released if atexit registration fails
- ✅ fix(eval): add automatic cleanup for temp directories
- ✅ fix(logmanager): store TemporaryDirectory instance to prevent resource leak
- ✅ fix(eval): move init_tools outside inner function to avoid repeated calls
- ✅ fix(eval): use UUID for unique agent IDs
- ✅ fix(eval): prevent race condition in result retrieval
- ✅ fix(eval): add path traversal protection to FileStore.upload()
- ✅ fix(eval): use explicit shell invocation instead of shell=True
- ✅ fix(util): use ContextVar for thread-safe interrupt state
- ✅ fix(llm): explicitly close stream generator in finally block
- 🔄 fix(eval): add thread-safe locking for environment variable mutation
- 🔄 fix(chat): resolve thread-safety and resource leak issues
- ✅ fix(browser): close browser contexts to prevent resource leaks
- ✅ fix(tools): add defensive checks for edge cases
- 🔄 fix(llm): add safe parsing for environment variables

### gptme-contrib

- 🔄 feat(plugins): add attention-router and attention-history plugins
- ✅ feat(lessons): improve keyword specificity for 2 more lessons
- ✅ feat(lessons): improve keyword specificity for 8 lessons
- ✅ fix(gptmail): RFC 2047 encode Subject and From headers for non-ASCII chars
- ✅ feat(packages): add gptmail - email automation for gptme agents
- ✅ feat(tasks): add --user flag to filter tasks by assigned_to
- ✅ feat(patterns): add agent visual identity establishment lesson

