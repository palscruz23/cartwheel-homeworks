# HW3 Part C dimensions

This plan reconstructs the Part A dimensions from `pilot_scenarios.jsonl` and
`hw3-progress.md`; a separate original Part A plan was not found. The student
explicitly authorized final generation using these dimensions and proceeding
without the full five confirmed pilot failures. That exception does not mark
the incomplete pilot review as completed or change its human assessments.

The grounded plans are saved in `support_plan.json`. Their observed composition
is recorded in `generation_audit/plan_summary.json`.

| Dimension | Values |
| --- | --- |
| Authenticated role | shopper, merchant, support |
| Intent | order_status, refund, cancellation, policy_question, product_search, dispute, out_of_scope |
| Record involved | order, product, store_policy_page, none |
| Order status | placed, shipped, delivered, cancelled, refunded; not_applicable otherwise |
| Age since placement | 0–7, 8–14, 15–30, 31–60, 61+ days; not_applicable otherwise |
| Applicable policy | platform policies, store overrides, none |
| Tools needed | none, one_lookup, several_calls |
| Difficulty | well_specified, missing_information, ambiguous, boundary |
| User style | neutral_conversational, terse_fragmentary, typo_heavy, confused_rambling, frustrated_impatient, repetitive_pressuring, operational_shorthand, requests_short_plain_answer |

Each record also carries authenticated user and record identifiers and an exact
turn count. Turn count is a per-conversation property rather than an independent
dimension. Final conversations have one to three scripted user messages.

## Composition

- 175 coverage scenarios and 75 challenge scenarios.
- The challenge pool includes five read-only scenarios for each of the six
  documented data quality cases (30 scenarios), 15 refund boundary scenarios,
  10 store-override policy questions, five cancellation boundaries, five
  multi-turn order clarifications, five authorization boundaries, and five
  repeated out-of-scope requests.
- Every refund or cancellation targets a distinct order that is not referenced
  by another final scenario. Pinned lecture orders and pilot order targets are
  excluded from these operations. Damaged-record scenarios only request reads.
- Order ages and expected eligibility use the deterministic course-world anchor
  `seed.generate.WORLD_ASOF` (2026-07-01), not the machine's current date.
- Objective answers are grounded in database records, policy documents,
  `facts.yaml`, the supplied eligibility function, or `data_quality_cases`.
  Human-judgment expectations cite `SPEC.md`.
- Generation inputs exclude actual identifiers, dates, hidden expectations,
  eligibility decisions and internal policy answers. Literal `[ORDER]` and
  `[PRODUCT]` references are bound to verified identifiers after critique.

## Human review

Review 15 complete final conversations before running Cartwheel. Cover both
scenario groups, all three roles and every intent. Keep decisions in
`support_review.jsonl` using `scenario_id`, `decision` (`accept`, `revise`, or
`reject`), `reason`, and `change`. The coding agent does not fill in human
assessments. Apply revisions and replace rejected scenarios before execution.
