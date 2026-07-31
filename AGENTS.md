# AGENTS.md

## Mission

Produce the simplest correct solution that satisfies the user's request.

Optimize for:

* correctness
* maintainability
* readability
* reproducibility
* developer time

Do **not** optimize for cleverness or unnecessary sophistication.

---

# Core Philosophy

Prefer solving today's problem well over designing for hypothetical future requirements.

When multiple solutions are equally correct:

Choose the one that is:

* easier to understand
* easier to maintain
* easier to explain in an interview

Avoid complexity whose only purpose is looking "advanced."

---

# Planning

Before writing code:

1. Understand the actual problem.
2. Identify constraints.
3. Propose the minimum viable implementation.
4. Only then begin coding.

For tasks involving multiple files or architectural decisions:

* explain the plan first
* describe important trade-offs
* keep implementation incremental

---

# Simplicity First

Follow YAGNI.

Do not implement features that are merely anticipated.

Avoid adding abstractions until duplication or complexity clearly justifies them.

Whenever adding a new abstraction, ask:

> What concrete problem does this solve today?

If the answer is unclear:

Do not introduce it.

---

# Overengineering Guardrails

Avoid introducing:

* unnecessary design patterns
* factories with one implementation
* dependency injection without multiple implementations
* managers/controllers/services that only wrap one function
* generic frameworks for project-specific logic
* excessive configuration
* premature optimization

Prefer plain Python over architecture.

Delete code instead of abstracting it whenever reasonable.

---

# Token Efficiency

Assume context is expensive.

Prefer:

* minimal diffs
* editing existing files
* concise explanations
* focused answers
* localized changes

Avoid:

* rewriting entire files for small edits
* repeating unchanged code
* unnecessary boilerplate
* verbose summaries
* explaining obvious language syntax

When modifying existing code:

Return only the affected sections whenever practical.

---

# Python

Prefer:

* Poetry
* pathlib
* dataclasses when appropriate
* type hints where they improve clarity
* logging instead of print
* descriptive names
* small focused functions

Avoid:

* global mutable state
* unnecessary wrappers
* deep inheritance
* helper classes with only one consumer

---

# Repository Structure

Favor simple layouts.

Example:

```
src/
tests/
configs/
docs/
data/
models/
```

Avoid deep folder hierarchies unless they genuinely improve organization.

---

# Machine Learning

Always verify:

* target leakage
* train/test contamination
* duplicate samples
* missing values
* class imbalance
* feature distributions
* metric suitability

Never preprocess using information from the test set.

Keep experiments reproducible.

Prefer deterministic pipelines when possible.

Whenever choosing a model, explain:

* why it was selected
* why alternatives were rejected
* why the evaluation metric matches the business problem

---

# Data Science Workflow

Encourage:

* reproducible experiments
* configuration over hardcoded values
* clear separation between data, features, models and evaluation

Flag:

* data leakage
* suspicious validation performance
* unrealistic metrics
* hidden assumptions

Challenge questionable methodology instead of accepting it.

---

# Documentation

Document:

* why

More than:

* what

README should answer within approximately one minute:

1. What problem exists?
2. What approach was taken?
3. What result was achieved?
4. Why does it matter?

Move implementation details into `/docs`.

Avoid README bloat.

---

# Reviews

Before considering work complete, verify:

* correctness
* readability
* maintainability
* reproducibility
* performance
* edge cases

Then ask:

1. Can this be simpler?
2. Can code be deleted?
3. Is this solving today's problem?
4. Is every new file justified?
5. Would a hiring manager understand this quickly?

If not:

Simplify.

---

# Portfolio Bias

When multiple implementations are equally good:

Prefer the one that:

* demonstrates practical engineering
* follows common industry conventions
* is straightforward to explain
* minimizes maintenance burden
* highlights sound engineering judgment

Never add complexity simply to make the project appear more advanced.

---

# Communication Style

Be concise.

Challenge questionable assumptions.

State trade-offs explicitly.

Do not automatically agree with implementation choices.

Recommend simpler solutions whenever appropriate.

If uncertain:

Say so instead of guessing.
