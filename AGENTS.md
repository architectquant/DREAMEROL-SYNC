# AGENTS.md
# Project Rules, Development Safety, Context Optimization & Daily Logging

## 1. GENERAL WORKING PRINCIPLES

- Work in small, logical and independently verifiable steps.
- Before changing code, inspect the existing implementation and identify the exact files involved.
- Understand how the current functionality works before modifying it.
- Make the smallest necessary change.
- Preserve existing working functionality.
- Do not rewrite or restructure working code without a clear technical reason.
- Do not modify unrelated files or introduce unnecessary dependencies.
- Reuse the existing project architecture, conventions and test framework.
- Prefer short, clear and factual reports.
- Avoid unnecessary repeated analysis and file reading.

## 2. CRITICAL PROJECT PROTECTION RULES

The following functionality must be protected:

- Authentication and OAuth.
- Auth Broker (`auth_broker/*` and `/api/auth/*`).
- Login and profile switching.
- GitHub App installation and permissions.
- Fork discovery.
- Core synchronization algorithm.
- Existing safety checks and permission validation.

Do not modify these components unless the task explicitly requires it and the technical reason is clearly established.

Before any potentially risky change:
1. Inspect the existing implementation.
2. Identify dependencies and shared components.
3. Explain the risk.
4. Ask for approval before destructive or potentially breaking changes.

If a component is shared with working functionality, preserve it.

## 3. DAILY WORK LOG

Maintain a chronological daily log in: `docs/WORKLOG/`

### Rules

- Create or update `LOG_DD-MM-YY.md` (example: `LOG_16-11-26.md`).
- Check the actual system date and local time through the terminal before writing.
- Add a new entry immediately after each completed code modification, file creation or significant implementation step.
- NEVER overwrite or delete existing entries.
- Always append new entries at the bottom.
- All daily log entries must be written in Bulgarian.
- Keep entries short and factual.

### Entry format

### [HH:MM] - Кратко заглавие на промяната
- **Променени файлове:** списък с файловете.
- **Детайли:** 1–2 кратки изречения какво и защо е направено.

## 4. PROJECT DOCUMENTATION

Maintain the following document in `docs/developement/` without unnecessary duplication.

### A. CHANGELOG_AI.md — Completed Tasks

Update only after a major feature or bugfix is fully completed.

Include:
- Date and time.
- Completed task.
- Changed files.
- Reason for changes.
- Tests actually executed.
- Actual test results.
- Remaining issues or limitations.

Do not duplicate every small implementation step. Those are already recorded in the daily log.

### B. WORKLOG.md — Current Project State

This is the single source of truth for the current development state.

Update it:
- When a session ends.
- When work is interrupted.
- When a significant project state change occurs.

It must contain:
- Last completed task.
- Current Git branch and HEAD, when verified.
- Actual Git status and uncommitted changes.
- Completed and unfinished work.
- Known errors and limitations.
- Last executed tests and their actual results.
- Exact next development step.

### C. DECISIONS.md — Technical Decisions

Use this document: in main root, when a genuinely new architectural or important technical decision is made.

Record:
- The decision.
- The reason.
- Its consequences.

Do not use it as another daily log.

### Documentation rules

- Never record passwords, API keys, tokens, credentials or secrets.
- Never present assumptions as confirmed facts.
- Never claim that tests passed unless they were actually executed.
- Keep all documentation concise, accurate and verifiable.
- Avoid repeating the same information across documents.

## 5. SESSION MANAGEMENT

### Starting a new session

Before starting work:

1. Read `docs/WORKLOG/WORKLOG.md`.
2. Check the latest relevant daily log entries.
3. Read relevant entries in `CHANGELOG_AI.md` when necessary.
4. Check the actual Git state using `git status`.
5. Verify the documented state against the actual repository.
6. Continue from the exact recorded next step.

Never assume that the previous session's state is unchanged.

### Ending or interrupting a session

Before stopping:

1. Update the daily log.
2. Update `WORKLOG.md` with the actual project state.
3. Update `CHANGELOG_AI.md` only if a major task is completed.
4. Update `DECISIONS.md` only if a new important decision was made.
5. Check Git status and identify uncommitted changes.
6. Record the exact next step.

Keep one session focused on one coherent development objective.

A new session can be started using the OpenCode session controls (`Ctrl+X`, then `N`, when supported).

## 6. CONTEXT AND TOKEN OPTIMIZATION

- Work in small, completed steps.
- Avoid rereading files that have already been inspected unless necessary.
- Use existing logs and documentation to recover project context.
- Do not repeat successful checks without a technical reason.
- Prefer concise reports over lengthy explanations.
- Monitor context usage when the interface provides this information.

### /compact rules

- Use `/compact` when the conversation contains substantial outdated or repetitive context.
- Approximately 40–50% context usage can be used as a guideline, not a mandatory threshold.
- Prefer compacting after a completed logical subtask.
- Before compacting, ensure that important work and decisions are documented.
- Preserve changed files, test results, known problems and the exact next step.
- Never compact during an unfinished code modification, running tests, active debugging or a critical multi-step operation.
- After compacting, continue from the preserved context without unnecessarily rereading the entire project.
- Never assume `/compact` resets or extends AI provider usage limits.

When appropriate, suggest `/compact` to the user. Do not execute interactive commands without the necessary permission and interface support.

## 7. TESTING AND VALIDATION

- Run appropriate targeted tests after significant code modifications.
- Run the broader relevant test suite after completing a feature or bugfix.
- Use the existing project testing framework.
- Avoid unnecessary repeated test execution.
- Report actual results, including failures and warnings.
- If a test fails, identify the specific error and whether it is related to the current changes.
- Do not claim successful implementation when required tests have failed or have not been executed.

## 8. GIT SAFETY

NEVER execute the following operations without explicit user approval:

- `git commit`
- `git push`
- `git merge`
- Branch switching.
- History rewriting (`rebase`, `amend` and similar operations).

Additional rules:

- Never delete uncommitted changes.
- Never overwrite existing work without verification.
- Never modify Git history for documentation or logging purposes.
- Check Git status before potentially risky operations.
- Explain the consequences before performing destructive Git operations.

## 9. ERROR HANDLING AND ESCALATION

If instructions are unclear, requirements conflict or a change may damage existing functionality:

1. Stop before making the risky change.
2. Explain the specific problem.
3. Identify the affected functionality and files.
4. Suggest the safest solution.
5. Ask for approval when necessary.

Do not guess when guessing could cause code loss, regressions or security problems.

## 10. FINAL PRIORITY RULE

When speed, context optimization or convenience conflicts with project safety, ALWAYS prioritize:

1. Existing working functionality.
2. Security and data integrity.
3. Correctness of implementation.
4. Reliable testing and verification.
5. Accurate documentation.
6. Efficiency and context optimization.

**MAIN OBJECTIVE: Maintain a stable, secure and maintainable project through minimal changes, reliable tests, clear documentation and complete control over modifications.**