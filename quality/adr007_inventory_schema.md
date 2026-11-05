# ADR-007: mandatory replacement inventory (not yet automated)

For each replaced component, supply an approved, version-controlled inventory:
- **Scope:** old component and exact replacement boundaries.
- **Old HTML/CSS/JS structures:** exact IDs/selectors/function names, with file and location.
- **Disposition:** removed or retained, with rationale for every retained item.
- **Forbidden remnants:** exact names/patterns tested in the new source, not just CSS visibility.
- **Business logic retained:** tests demonstrating preservation.
- **New boundaries:** UI, domain, adapter interfaces and dependencies.
- **Evidence:** diff, architecture-test log, browser desktop/mobile screenshots, actual interaction/regression results.
- **Reviewer:** project owner sign-off.

A missing inventory or negative test is a release blocker. The current baseline pipeline does NOT implement this release check.
