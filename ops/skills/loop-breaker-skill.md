# Loop Breaker Skill

## Objective

Stop wasteful repetition early.

This skill is used when the project starts circling around the same blocker, repeating the same action pattern, or spending tokens without producing a better decision, a better artifact, or a working result.

## Core Rule

If two to three attempts on the same narrow problem do not produce meaningful progress, the problem is no longer an execution task.
It becomes an audit task.

## Trigger Conditions

Activate this skill when any of the following happens:

- the same task is retried multiple times with the same failure shape
- the same file or subsystem is being touched repeatedly without improving the result
- prompts, scripts, or checks keep returning the same weak outcome
- subagents keep producing restatements instead of new leverage
- the plan is still moving, but the product is not

## Mandatory Response

When a loop is detected:

1. Stop repeated execution on that exact path.
2. Reframe the issue as a defect in assumptions, architecture, process, or instrumentation.
3. Assign the Quality Auditor to identify the failure mode.
4. Convert the audit into one concrete diagnosis.
5. Assign the Builder / Engineer to implement the smallest high-leverage fix.
6. Re-test only the changed path.
7. If the fix works, continue the main plan.
8. If the fix fails again, escalate to the Chief Technical Architect or Product Strategist depending on the root cause.

## Escalation Map

Use the Quality Auditor when:

- failures are inconsistent
- the team may be missing the real bug
- output quality is regressing without obvious code breakage

Use the Chief Technical Architect when:

- the same failure comes from structure, not from a local bug
- a module boundary is wrong
- state, persistence, or lifecycle design is the true blocker

Use the Product Strategist when:

- the team keeps shipping activity but not value
- the flow is technically working but still weak, confusing, or generic
- too many branches or surfaces are diluting the wedge

Use the Design Director when:

- the product works but still feels cheap, confusing, or template-like

## Iteration Budget

Default budget before forced escalation:

- 2 tries for the same local bug or patch pattern
- 2 prompt tweaks for the same weak LLM behavior
- 1 architecture debate if the code already shows structural fragility

After the budget is spent, stop repeating and switch to diagnosis.

## Success Standard

A loop is considered resolved only when one of these is true:

- the blocker is removed
- the root cause is identified and documented
- the team has changed strategy instead of repeating the same tactic
