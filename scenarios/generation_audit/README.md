# HW3 Part C generation and critique audit

The shell could not resolve `api.openai.com` in this session. Generation and
critique therefore use separate coding-agent responses under the parallel-worker
option in `scenarios/skill/SKILL.md`. These are coding-agent calls, not observed
`gpt-4o-mini` API calls. No Cartwheel conversations are executed by this pipeline.

- `generation_inputs/<id>.json`: the user-visible plan supplied to generation.
- `generation/<id>.json`: the generation worker's saved draft response.
- `critic_inputs/<id>.json`: the draft, task, verification record, and comparison
  openings supplied to an independent critic worker.
- `critic/<id>.json`: the critic's saved response, including issues and changes.
- `plan_summary.json`: the planned dimension counts.

Each worker authors exactly one scenario per model response and saves it before
reading the next input. Workers swap
scenario assignments for critique so a worker does not critique its own draft.
A draft's mere existence is not evidence of a completed critic call. Only
existing critic output files count toward completed critiques. These records
preserve prompts and saved outputs; they are not provider API response envelopes
and do not contain provider request IDs, billing, token usage, or model internals.

## Generation instructions

Write one realistic support conversation with `opening_message` and `followups`.
Use the assigned role, goal, language style and exact turn count. Use literal
`[ORDER]` / `[PRODUCT]` placeholders for identifiers. Do not invent entity names,
amounts, dates or other facts. Each scripted followup must be plausible regardless
of the agent's preceding response. Never expose internal tools, traces, hidden
expectations or policy answers in simulated user messages.

## Critique instructions

Independently inspect one draft for hallucinated facts, response-dependent
followups, repetitive templates, unnatural language and style mismatches.
Preserve the goal, grounded references, requested amounts, and turn count.
Verification records may be read to check invented facts but must not be copied
into user messages as hidden knowledge. Save `opening_message`, `followups`, an
`issues` list, and a `changed` boolean. Unchanged valid drafts may have no issues.

The final dataset is assembled from critic outputs with verified identifier
bindings. Human scenario review is a separate pending activity; critic approval
does not stand in for the student's judgments.

## Current checkpoint and resumption

All 250 generation responses were saved. The coding-agent service reached its
usage limit after nine independent critique responses. The other 241 critiques
are pending, not implicitly approved. Each assembled scenario records its actual
`provenance.critic_status`; pending records have no critic output path.

`../support_scenarios.jsonl` contains all 250 generated conversations and passes
the final schema/composition checks. `../support_sample.md` contains 15 complete
conversations for human review, and `../monitoring_scenarios.jsonl` contains the
50 selected future-monitoring cases. Neither automated critique nor human review
is complete. Cartwheel has not been run on this dataset.

To finish only the remaining critiques from a terminal with model API access:

```bash
uv run python -m scenarios.finish_support_critique --model gpt-4o-mini
uv run python -m scenarios.assemble_support
uv run python -m scenarios.validate scenarios/support_scenarios.jsonl --final
```

The first command makes paid model calls (currently 241 pending conversations)
and reads `OPENAI_API_KEY` locally from `.env`. Add `--limit 5` to process a small
batch first. Completed critiques are preserved. New provider responses are
appended under `api_responses/`; original coding-agent responses remain intact.
No command above executes Cartwheel scenarios.

The assembler refreshes dataset and review-sample outputs, so finish critique
before recording human decisions. It checks saved output hashes and refuses to
overwrite files edited since assembly. It never writes `support_review.jsonl`.
Without `--allow-pending-critique`, it refuses assembly until all critiques exist.

Offline checks: final schema/composition validation; all referenced order/product
snapshots matched a freshly seeded temporary database; authenticated identities,
expected permissions, policy references, and distinct write targets checked;
12 existing scenario-validation tests passed. No live Cartwheel runs occurred.
