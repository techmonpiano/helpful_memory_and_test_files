# LLM Debugging Prompt Template
**Concise, effective instructions for troubleshooting/debugging**

---

## Copy-Paste Template for Bug Fixes

```
DEBUGGING PROTOCOL (MANDATORY):

1. Write unit test that reproduces the bug
2. Add debug logging to /tmp/debug_[feature].log at ALL decision points
3. Run test, analyze logs, identify root cause
4. Make ONE targeted fix based on log evidence
5. Verify test passes

CONSTRAINTS:
- DO NOT modify existing tests
- DO NOT guess or make multiple changes
- DO NOT skip logging step
- MUST identify root cause before fixing

Log format: timestamp, function_name, variables, branch_taken
```

---

## Copy-Paste Template for Feature Implementation

```
IMPLEMENTATION PROTOCOL:

Step 1 - Tests First:
- Write unit tests for all edge cases
- Save to tests/test_[feature].py
- DO NOT implement yet

Step 2 - Implementation (after test review):
- Implement to pass tests
- Add debug logging to /tmp/[feature]_debug.log
- DO NOT modify tests

Step 3 - Verification:
- All tests pass
- No duplicate code
- git diff review
```

---

## Copy-Paste Template for Analysis Only

```
ANALYSIS PROTOCOL (NO FIXES):

1. Add debug logging to /tmp/analysis_[timestamp].log
2. Log: input values, conditions evaluated, branches taken, output
3. Run 5 test cases
4. Report findings from logs
5. DO NOT fix anything - analysis only

Report format:
- What behavior is observed
- Where it diverges from expected
- Root cause hypothesis
```

---

## Quick Constraints Block (add to any prompt)

```
CONSTRAINTS:
- DO NOT modify existing tests
- DO NOT make multiple changes at once
- MUST log to /tmp/debug.log before fixing
- Break complex tasks into smaller steps
```

---

## Emergency Reset Instruction

```
CONTEXT RESET - Previous approach was incorrect.

New direction:
1. Ignore previous attempts
2. [State the specific task clearly]
3. Follow debugging protocol above
4. One fix only based on logs
```

---

## Usage Tips

- Copy relevant section above your actual request
- Be specific about what feature/bug you're addressing
- Always include CONSTRAINTS block
- Use Analysis template when unsure of root cause
- Use Emergency Reset if LLM goes wrong direction 2+ times
