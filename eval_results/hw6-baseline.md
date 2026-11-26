# HW6 baseline review

Observed live batch: 50 agent runs on `gpt-4o-mini`; 25 evaluations by accepted frozen `unnecessary_response_content-v2`, also on `gpt-4o-mini`. All 50 trials produced valid rewards with no infrastructure errors. These runs made 96 agent model requests; judge evaluations are counted separately.

Student classifications remain pending; `cases.jsonl` has no classification fields.

| Case | Mode | Passed | Trial outcomes |
| --- | --- | ---: | --- |
| e-001 | unnecessary_response_content | 1/5 | F F P F F |
| e-002 | unnecessary_response_content | 0/5 | F F F F F |
| e-003 | unnecessary_response_content | 0/5 | F F F F F |
| e-004 | unnecessary_response_content | 0/5 | F F F F F |
| e-005 | unnecessary_response_content | 5/5 | P P P P P |
| e-006 | missing_human_escalation | 1/5 | F F F F P |
| e-007 | missing_human_escalation | 0/5 | F F F F F |
| e-008 | missing_human_escalation | 0/5 | F F F F F |
| e-009 | missing_human_escalation | 0/5 | F F F F F |
| e-010 | missing_human_escalation | 0/5 | F F F F F |

P/F presentation follows trial start time, then trial name; baseline counts are independent of this ordering. This is not the Part E analysis.

The handout rule is regression for 5/5 and capability for any completed failure. Capability rates are the observed pass fractions. The student must review and record the final classifications.

See [machine-readable evidence](hw6-baseline.json) for exact trial names, verifier component scores, evidence paths and hashes. The original conversations and tool traces remain in the ignored local Harbor job directories.

The two setup-only error jobs are preserved separately; neither reached the agent or judge. No completed evaluation failure was rerun.

Offline verification: supplied case export, fresh-seed fact and authorization checks, accepted-v2 prompt/model equality, and baseline-summary/count consistency. Live verification: the 50 agent runs and 25 judge evaluations above.

Remaining: student classifications, Part B metrics, CI workflow and both same-PR runs, Part E 15-run comparison, and the student video.
