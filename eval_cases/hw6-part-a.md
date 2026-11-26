# HW6 Part A preparation

Ten draft cases in `cases.jsonl` retain the supplied Cartwheel schema.
The student approved the 50-run / 25-judge-evaluation baseline batch in this
session. All 50 trials completed with valid rewards and no infrastructure
errors. No case is classified in the case file; student review is pending.

The current HW4 review state approves both selected modes. Each case records
its exact source trace and scenario. The original HW4 labels and HW5 records
are preserved. The student explicitly accepted `unnecessary_response_content-v2`
for HW6 in this session; frozen later versions are not authorized substitutes.

| Cases | HW4 failure mode | Scenarios | Verifier |
| --- | --- | --- | --- |
| e-001–e-005 | unnecessary_response_content | support-0018, support-0136, support-0031, support-0008, support-0114 | Accepted frozen v2 plus exact code checks |
| e-006–e-010 | missing_human_escalation | support-0153, support-0172, support-0165, support-0162, support-0156 | Required escalate_to_human call under ESC-2/ESC-3 |

The escalation cases test the required tool execution, not the meaning or
quality of the final explanation. General dispute-policy questions were
excluded because they do not necessarily require opening a ticket.
`no_write_tools` is the supplied refund/cancellation check; it permits escalation.

## Observed offline verification

- The supplied exporter generated all ten baseline Harbor tasks.
- Source order/product facts matched a fresh seed in a temporary directory.
- Shopper ownership and merchant store scope matched those records.
- All five generated language verifiers matched v2's frozen prompt and model.
- Docker reported server version 29.5.3; Harbor reported 0.23.0.

Live baseline evidence is saved under the ignored `.harbor/jobs` tree. The
review report is `eval_results/hw6-baseline.md`, with exact trial records and
evidence hashes in `eval_results/hw6-baseline.json`. `e-005` passed 5/5;
`e-001` and `e-006` passed 1/5 each; the other seven cases passed 0/5.
The batch made 96 agent model requests and 25 judge evaluations. Student
classifications remain pending. No additional paid runs have been approved.

## Reproduce the accepted-judge export

The supplied exporter selects the highest frozen version of a mode. Until
explicit version pinning is addressed for CI, isolate the accepted record:

```bash
mkdir -p .harbor/hw6-v2-state/judges
cp analysis/state/judges/unnecessary_response_content-v2.json \
  .harbor/hw6-v2-state/judges/
CARTWHEEL_ANALYSIS_STATE="$PWD/.harbor/hw6-v2-state" \
  uv run python scripts/export_harbor_tasks.py --baseline
```

This uses the supplied adapter and leaves every HW5 record unchanged. Generated
tasks and isolated judge state stay under the ignored `.harbor` directory.

## Approved paid batch and pending review

Approved agent model: `gpt-4o-mini`, matching the existing configuration and
HW3 runs. Ten tasks × five attempts = 50 agent runs. Five tasks use v2,
with frozen judge model `gpt-4o-mini`: 25 judge evaluations. Provider requests
and tokens can vary with tool use or backend retries. The student approved this
specific batch with "approve"; this does not authorize later CI or Part E runs.

## Local execution notes

Harbor's first-run notification cache was read-only. A local ignored wrapper
redirects its cache paths into `.harbor/cache`. Docker's buildx cache was also
read-only, so `BUILDX_CONFIG` points to `.harbor/buildx`. The configured Windows
Docker credential helper then failed for the public base image; an isolated
`DOCKER_CONFIG` under `.harbor/docker-config` uses public image access. Existing
Docker settings and credentials were not changed. The setup-only failed jobs
are preserved as `hw6-infra-e-001-buildx-readonly` and
`hw6-infra-e-001-desktop-credentials`; neither reached the agent or judge.

The live jobs are `hw6-baseline-e-001` (five trials) and
`hw6-baseline-e-002-through-e-010` (45 trials). Automatic trial retries are
disabled. Completed failures are retained as evidence.

This Harbor installation omits `trial_results` from its root job result and
stores each trial in its own result file. Baseline summary inputs are collected
under `.harbor/reports`, with source jobs and ordering documented; original
Harbor result files remain unchanged. Baseline counts do not depend on trial
order. Part E will need to preserve Harbor's actual result ordering explicitly.

After execution, summarize each case's five trials. Infrastructure errors or
missing rewards prevent classification. The student records `regression` for
5/5 passes, or `capability` and its observed pass fraction for any completed
failure. Add cases if necessary to obtain both kinds; never change a recorded
outcome to force the required mix. Parts B–E and the video remain pending.
