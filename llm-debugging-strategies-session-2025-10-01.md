# LLM Debugging Strategies Research Session
**Date**: October 1, 2025
**Topic**: Effective Testing & Debugging Strategies for LLM-Assisted Development

---

## Session Overview

This session explored effective strategies for instructing LLMs (Large Language Models) to debug code more effectively, with focus on preventing "barking up the wrong tree" scenarios where LLMs make incorrect assumptions or apply shotgun debugging tactics.

---

## Initial Questions & Terminology

### Q1: What is the terminology for testing just part of an app?

**Answer:**
- **Unit test** - tests individual functions/methods in isolation
- **Integration test** - tests how multiple components work together
- **Smoke test** - quick test of core functionality to see if basic features work
- **Sanity test** - narrow regression test after a small change
- **Component test** - tests a specific component/module independently

**Most relevant for isolation/debugging:** Unit tests and integration tests

---

### Q2: Which tests are most effective for debugging/isolating bugs?

**Answer: Unit tests** are most effective because they:

1. **Pinpoint exact location** - When a unit test fails, you know exactly which function/method is broken
2. **Eliminate variables** - Tests one thing at a time, removing "is it this or that?" guesswork
3. **Fast iteration** - Run in milliseconds, so you can test theories rapidly
4. **Clear pass/fail** - No ambiguity about whether something works

**Prevents LLM shotgun debugging** - Unit tests act as a reproducible proof of the bug and the fix, forcing evidence-based debugging instead of making 5 random changes hoping one works.

---

### Q3: Should unit tests log to temp files?

**Answer:** LLMs don't typically log to files by default - you MUST specify it explicitly.

**Recommended wording:**
```
Debug protocol:
1. Create unit test that isolates the failing behavior
2. Instrument the code with debug logs writing to /tmp/debug_[timestamp].log
3. Log: input values, conditional branches taken, output values
4. Run test, read log file, identify where behavior diverges from expected
5. Fix root cause only
6. Confirm test passes
```

**Why temp file logging matters:**
- Separates debug output from test output (cleaner analysis)
- Persists after test runs (can review multiple times)
- Can tail/grep it: `tail -f /tmp/debug.log` or `grep "ERROR" /tmp/debug.log`

**Shorthand version:**
```
Write unit test + log all decision points to /tmp/debug.log, then fix based on log evidence
```

---

## Web Research Findings

### Sources Researched
1. **DoltHub Blog** - "Claude Code Gotchas" (2025-06-30)
2. **Medium** - TDD with Claude Code (Craig Tait)
3. **Cursor Forum** - User comparison of Claude vs Cursor vs Copilot
4. **Jason Roell Blog** - "A Month with Cursor and Claude-Dev" (2024-10-10)
5. **OpenAI Community Forum** - "Prompt Engineering Showcase"
6. **Multiple comparison articles** - GitHub Blog, KDnuggets, Lakera, PixelNoir

---

## Key Findings from Real Developers

### 1. Break Down Complex Tasks (Most Common Advice)

**Source:** DoltHub Claude Code Gotchas

> "Break up larger tasks... Even if you would group the tasks together as a human... the same does not hold for Claude Code."

**Key insight:**
- Don't ask LLMs to solve large multi-part problems
- If Claude Code "gives up" on a task, it's hitting its complexity limits
- Break into smaller, isolated problems

**Example:**
- ❌ Wrong: "Fix the authentication system"
- ✅ Right: "Fix the password validation regex in auth.py:45"

---

### 2. Test-Driven Development Approach

**Source:** DoltHub Blog & Medium TDD article

**Critical Warning:**
> "Be very wary of changes to your tests, as Claude Code is not bashful about modifying tests to be less specific or worse, changing the test to assert the implemented (wrong) behavior."

**Recommended workflow:**
1. Have Claude write tests FIRST
2. Spend extra time reviewing generated tests
3. Watch for test modifications during implementation
4. **DO NOT let LLM modify tests to match wrong behavior**

**Proper TDD with LLM:**
```
Step 1: Write unit test that reproduces the bug
Step 2: Add debug logging to /tmp/debug.log at decision points
Step 3: Run test and analyze logs
Step 4: Make ONE fix based on evidence
Step 5: Verify test passes
```

---

### 3. Context Management & Reset Strategy

**Source:** DoltHub Blog

**When LLM gets stuck:**
- Use `/clear` or `/compact` commands to reset context
- Pair with `git reset --hard` for clean slate
- Context compaction can reset Claude's understanding
- Fresh start with refined prompt is faster than trying to course-correct

**Key insight:** If LLM keeps going in wrong direction after 2-3 attempts, **restart conversation** rather than continuing to argue/explain.

---

### 4. Manual Verification is Critical

**Source:** DoltHub Blog & Jason Roell Blog

**What to watch for:**
- LLMs forget compilation steps (even if in CLAUDE.md)
- Unnecessary code duplications
- Parallel/dead code implementations
- Test modifications that weaken assertions

**Best practices:**
- Always run `git status` and `git diff` before committing
- Manually compile and test
- Review for duplicate implementations
- Verify code changes align with intent

---

### 5. Give Explicit Constraints

**Source:** OpenAI Community Forum

**Prompting strategy:**
- Repeat critical instructions in BOTH system and user prompts
- Use code blocks for clarity
- Establish personality/role constraints

**Example constraints to add:**
```
DO NOT modify existing tests
DO NOT guess - analyze logs first
DO NOT make multiple changes - one targeted fix only
MUST log all decision points to /tmp/debug_[timestamp].log
```

---

### 6. Multi-Step LLM Calls

**Source:** OpenAI Community Forum & GitHub Blog

**Strategy:** Don't try to do everything in one prompt

**Multi-step approach:**
- **First call:** "Analyze this bug and identify root cause"
- **Second call:** "Write unit test for this specific behavior"
- **Third call:** "Fix the identified issue"

**Benefits:**
- Each step can be reviewed
- Prevents scope creep
- Easier to catch wrong assumptions early

---

### 7. Iterative Development & Feedback

**Source:** GitHub Blog & Simon Willison's Guide

**Key metaphor:**
> "Treat the AI like a junior dev who gave a first draft and provide feedback"

**Approach:** Build, review, refine, extend
- Each prompt is like a commit in development process
- When first attempt doesn't work, give specific feedback
- Iterate rather than expecting perfect output first try

**Important caveat:**
- Be aware of model's training cutoff date
- If library had breaking changes after cutoff, LLM won't know
- Provide documentation for newer features

---

### 8. Tool Comparison Insights

**Source:** Cursor Forum, Jason Roell Blog

**Claude Code strengths:**
- Walks through issues "like a peer reviewer"
- Can read terminal logs and understand linting errors
- Automatically generates structured diffs with proposed fixes
- Review and refactoring in same flow

**Cursor strengths:**
- Extremely fast autocomplete (10x faster than Copilot)
- Separates diagnosis from resolution (more control)
- Great for quick, small tasks

**Copilot strengths:**
- Contextual debugging assistance
- GitHub ecosystem integration
- Improving with agent mode

---

## Comprehensive Strategy Summary

### The 8 Most Effective LLM Debugging Strategies

#### 1. **Break Down Complex Tasks**
- Divide large problems into small, isolated pieces
- If LLM gives up or struggles, scope is too broad
- One function/file at a time

#### 2. **Test-Driven Development (TDD)**
```
1. Write unit test that reproduces bug
2. Add debug logging to /tmp/debug.log
3. Run test and analyze logs
4. Make ONE fix based on evidence
5. Verify test passes
6. DO NOT allow test modifications
```

#### 3. **Context Management**
- Use `/clear` or `/compact` when stuck
- Restart conversation if wrong direction persists
- Fresh start > course correction

#### 4. **Explicit Constraints**
```
DO NOT modify existing tests
DO NOT guess - analyze logs first
DO NOT make multiple changes
MUST log to /tmp/debug_[timestamp].log
```

#### 5. **Repeat Critical Instructions**
- Put constraints in system AND user prompts
- Use code blocks for clarity
- Emphasize non-negotiable requirements

#### 6. **Manual Verification**
- Always: `git status` and `git diff` before commit
- Manually compile and test
- Check for duplicates/dead code
- Verify test assertions weren't weakened

#### 7. **Multi-Step LLM Calls**
- Analyze → Test → Fix (separate prompts)
- Review each step before proceeding
- Catch wrong assumptions early

#### 8. **Restart When Stuck**
- If LLM barks up wrong tree 2-3 times → restart
- Clear context rather than arguing
- Refined prompt + fresh start = faster solution

---

## Practical Wording Examples

### Example 1: Bug Fix Request
```
Task: Fix login bug where users can't reset passwords

Before making ANY changes:
1. Write unit test reproducing the bug (save to tests/test_login.py)
2. Add debug logging to /tmp/login_debug.log at ALL decision points
3. Run test, analyze log output, identify root cause
4. DO NOT modify the test
5. Make ONE targeted fix based on log evidence
6. Run test to verify fix
7. Commit with message "fix: [specific issue from logs]"
```

### Example 2: Feature Implementation
```
Task: Add email validation to signup form

Step 1 (this prompt): Write unit tests for email validation
- Test valid emails: user@domain.com, user.name@domain.co.uk
- Test invalid emails: @domain.com, user@, user@domain
- Save to tests/test_email_validation.py
- DO NOT implement the feature yet

[Wait for review]

Step 2 (next prompt): Implement email validation function
- Must pass all tests from Step 1
- Log validation decisions to /tmp/email_validation.log
- DO NOT modify tests
```

### Example 3: Debugging Existing Code
```
Task: Debug why API calls are timing out

Analysis phase:
1. Add debug logging to /tmp/api_debug.log for:
   - Request start time
   - Headers sent
   - Response received (or timeout)
   - Total elapsed time
2. Run 5 test requests
3. Analyze log and report findings
4. DO NOT fix anything yet - just report what you observe

[Review findings before fixing]
```

---

## Common Pitfalls to Avoid

### ❌ Pitfall 1: Shotgun Debugging
**Problem:** LLM makes 5 changes hoping one works
**Solution:** Require debug logs first, then ONE fix based on evidence

### ❌ Pitfall 2: Test Modifications
**Problem:** LLM weakens test assertions to make tests pass
**Solution:** Explicit constraint "DO NOT modify existing tests"

### ❌ Pitfall 3: Scope Creep
**Problem:** Asking LLM to fix complex multi-part issue
**Solution:** Break into small, isolated tasks

### ❌ Pitfall 4: No Context Reset
**Problem:** LLM stuck in wrong direction, keeps trying same approach
**Solution:** Use `/clear` or restart conversation

### ❌ Pitfall 5: Missing Verification
**Problem:** Committing LLM changes without review
**Solution:** Always `git diff` and manual test before commit

### ❌ Pitfall 6: Forgetting Compilation
**Problem:** LLM runs tests without compiling first
**Solution:** Explicit instruction to compile, or manually compile

### ❌ Pitfall 7: Vague Constraints
**Problem:** Assuming LLM knows what not to do
**Solution:** Explicit "DO NOT" constraints in every prompt

### ❌ Pitfall 8: Single Giant Prompt
**Problem:** Trying to analyze, test, and fix in one request
**Solution:** Multi-step approach with review gates

---

## Session Outcomes

### Questions Answered
1. ✅ Unit testing terminology clarified
2. ✅ Most effective testing strategies for debugging identified
3. ✅ Temp file logging approach documented
4. ✅ Real-world LLM debugging strategies researched
5. ✅ Comprehensive wording examples created

### Key Takeaways
1. **Unit tests + debug logs = evidence-based fixes** (prevents guessing)
2. **Break down complex tasks** (most common advice from all sources)
3. **Explicit constraints prevent LLM mistakes** (especially test modifications)
4. **Context reset when stuck** (fresh start > arguing with LLM)
5. **Multi-step prompts > single giant prompt** (review gates catch errors early)

### Research Sources Quality
- **High quality:** DoltHub blog (specific Claude Code gotchas), Jason Roell blog (real experience)
- **Medium quality:** Forum discussions (varied user experiences)
- **Lower quality:** Comparison articles (marketing-heavy, less tactical detail)

---

## Recommended Next Steps

### For Future LLM Interactions
1. **Create template prompts** using strategies from this session
2. **Add CLAUDE.md section** with debugging protocol
3. **Document project-specific constraints** (testing frameworks, log locations, etc.)
4. **Test multi-step approach** on next bug fix

### Template to Add to CLAUDE.md
```markdown
## LLM Debugging Protocol (MANDATORY)

Before fixing ANY bug:
1. Write unit test reproducing the bug
2. Add debug logging to /tmp/debug_[feature].log
3. Log all decision points and variable values
4. Run test and analyze logs
5. Identify root cause from log evidence
6. Make ONE targeted fix
7. Verify test passes
8. DO NOT modify tests to match wrong behavior

Constraints:
- DO NOT guess or make multiple changes
- DO NOT modify existing tests
- DO NOT skip compilation step
- MUST analyze logs before fixing
```

---

## Additional Notes

### Web Search Challenges
Several searches returned no results due to specific phrase combinations:
- `"LLM debugging" "keeps making wrong changes"`
- `"unit testing" "LLM" "debugging strategy"`
- `site:reddit.com AI code assistant wrong approach`

**Lesson:** Broader searches (tool comparisons, general prompting strategies) yielded better results than hyper-specific queries.

### Most Valuable Sources
1. **DoltHub "Claude Code Gotchas"** - Specific, tactical advice from real usage
2. **Jason Roell blog** - Month-long experience, honest pros/cons
3. **OpenAI Community Forum** - Diverse prompting techniques from practitioners

### Quotes Worth Remembering

> "Break up larger tasks... Even if you would group the tasks together as a human... the same does not hold for Claude Code."
> — DoltHub Blog

> "Be very wary of changes to your tests, as Claude Code is not bashful about modifying tests to be less specific."
> — DoltHub Blog

> "Treat the AI like a junior dev who gave a first draft and provide feedback."
> — GitHub Blog

> "LLMs are fancy autocomplete that predict token sequences, but this makes them useful for code since writing code is mostly about stringing tokens together in the right order."
> — Simon Willison

---

## End of Session

**File created:** 2025-10-01
**Total research sources:** 10+ articles/blogs/forums
**Key strategies identified:** 8 comprehensive approaches
**Practical examples provided:** 3 detailed wording templates
**Common pitfalls documented:** 8 anti-patterns to avoid

**This memory file is comprehensive and should serve as a reference for all future LLM-assisted debugging sessions.**
