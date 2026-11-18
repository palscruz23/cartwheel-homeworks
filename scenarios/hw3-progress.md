# Homework 3 progress

- Setup, running services, and connection check reported complete by the student.
- Dimension plan agreed, including explicit order status and placement-age ranges: 0–7, 8–14, 15–30, 31–60, 61+.
- Read all six data quality cases from the local database.
- Prepared 30 grounded plans in pilot_plan.json: 18 coverage and 12 challenge; all three roles, seven intents, five statuses, five age ranges, and six damaged-record cases.
- Generation blocked by DNS resolution of api.openai.com in the assistant execution environment. No successful model responses observed.
- Next: run `uv run python scenarios/generate_pilot.py` from the repository root where model network access is available, then run `uv run python -m scenarios.validate scenarios/pilot_scenarios.jsonl`.
- Human must review complete conversation samples before the pilot runner starts.

## Deliverables (all pending)

- [x] scenarios/pilot_scenarios.jsonl
- [ ] scenarios/pilot-results.jsonl
- [ ] scenarios/pilot_review.jsonl (student decisions; at least 10 reviews and 5 confirmed failures)
- [ ] scenarios/support_scenarios.jsonl
- [ ] scenarios/support_review.jsonl (15 student reviews)
- [ ] scenarios/monitoring_scenarios.jsonl
- [ ] scenarios/final-results.jsonl
- [ ] reports/smoke-output.txt
- [ ] traces/support_traces.json
- [ ] Final validation and export checks, including inspection of 3 complete traces
- [ ] Student video, at most 5 minutes

## Latest repair

- Preserved the misnamed plans file as `scenarios/pilot_scenarios.plans-backup.json`.
- Restored missing `scenarios/pilot_plan.json` from that backup (30 plans).
- `uv` could not write its default cache in this session; used `.venv/bin/python` to start generation instead.
- Model service DNS lookup failed: `Temporary failure in name resolution`. No generated conversations observed.
- Next: run `uv run python scenarios/generate_pilot.py` from a terminal with model network access, then validate and review a sample before running Cartwheel.

## Pilot generation completed

- Created `scenarios/pilot_scenarios.jsonl`: 30 unique scenarios, 18 coverage and 12 challenge, including all six damaged-record cases.
- Used separate coding-agent turns for 30 generation calls, then 30 independent critic calls through two fresh reviewers. Expected metadata was withheld from generators.
- Offline validator passed with `UV_CACHE_DIR=/tmp/cartwheel-uv-cache uv run --offline python -m scenarios.validate scenarios/pilot_scenarios.jsonl`.
- Offline checks passed for authenticated identities, permissions, all order statuses and placement-age ranges, damaged-record references, and distinct records for refund/cancellation requests.
- Sample saved in `scenarios/pilot_sample.md`, covering both groups, all three roles, multiple styles, a state-changing request, damaged data, and the longest conversation (3 turns).
- Next required human gate: accept or revise the sample before running Cartwheel. No pilot executions or failure assessments have occurred.

## Part C generation checkpoint

- Student explicitly authorized Part C generation despite the incomplete pilot
  failure review. Existing pilot artifacts and human decisions were preserved.
- Reconstructed dimensions from the pilot tuples and earlier progress note;
  saved `scenarios/support_dimensions.md` and 250 grounded plans in
  `scenarios/support_plan.json`.
- Generated 250 conversations: 175 coverage and 75 challenge, including five
  cases for each of the six damaged records. Generation inputs and responses
  are saved separately under `scenarios/generation_audit/`.
- Nine independent critiques saved. Coding-agent service usage limit interrupted
  critique; 241 remain pending and are explicitly marked in scenario provenance.
  A resumable API helper and assembly command are documented in the audit README.
- Saved `support_scenarios.jsonl`, `monitoring_scenarios.jsonl` (50 cases),
  `support_sample.md` (15 complete conversations), and an unfilled
  `support_review_template.jsonl`. Actual human decisions remain pending;
  `support_review.jsonl` has not been fabricated.
- Final offline validator passed: 250 unique IDs, 175 coverage, 75 challenge,
  30 documented-defect cases. All order/product snapshots matched a freshly
  seeded temporary database. Identity, authorization, policy references, and
  unique write targets checked. Existing scenario-validation tests: 12 passed.
- No working database reset, final Cartwheel runs, model-based agent evaluation,
  trace export, or student recording performed. Generation is complete;
  automated critique and the required human review are incomplete.
