# QS governance and production release policy

Status: **NOT CERTIFIED FOR PRODUCTION RELEASE**.

## Current verified GitHub protection (2026-11-05)
- Active repository ruleset `pin2map – Produktionsschutz`, targeting `main` only.
- PR required; no bypass actors; deletion and force pushes blocked.
- `baseline-quality` required and must be current.
- Zero approving reviews required. **Therefore an owner can merge QA-only changes after passing tests without a separate approval.**

## Critical trust limitation
The `baseline-quality` workflow and its test scripts are part of the PR branch.
A PR can alter or weaken the workflow itself. A green status alone cannot certify
that the quality policy was preserved. CODEOWNERS without a required independent
review is insufficient. A sole repository owner cannot approve their own PR as
a distinct reviewer.

## Mandatory owner checklist before any merge
1. Confirm diff touches no production files. If it does, **do not merge** until
   ADR-007, ADR-008, interaction and regression release gates exist.
2. Independently inspect any changes to `.github/workflows/`, `quality/`,
   `tests/` and CODEOWNERS, and ensure no tests or job requirements are removed.
3. Inspect both PR check logs and saved desktop/mobile screenshots.
4. Check the ADR-007 inventory and removal proof for any replaced component.
5. Check ADR-008 dependency boundaries and real behavior tests.
6. Explicitly authorize the merge only after all requirements are satisfied.

## Stronger protection to configure
Use a second trusted reviewer (with repository access) and require at least one
approving review for `main`, including CODEOWNERS review for QS paths.
Alternatively, establish a separately protected approval process outside the
mutable PR workflow. Do not enable a one-review requirement without an
eligible second reviewer: it could block the sole owner from merging.

This document is guidance and evidence; **it does not enforce human approval**.
