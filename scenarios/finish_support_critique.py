"""Resume saved HW3 critiques with OpenAI; never execute Cartwheel scenarios.

Run from the repository root, then run ``python -m scenarios.assemble_support``.
Existing critique responses and all generation drafts are preserved.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI


async def run(model: str, workers: int, limit: int | None) -> int:
    audit = Path("scenarios/generation_audit")
    pending = [
        path
        for path in sorted((audit / "critic_inputs").glob("support-*.json"))
        if not (audit / "critic" / path.name).exists()
    ]
    if limit is not None:
        pending = pending[:limit]
    print(f"Model: {model}; pending critic calls in this batch: {len(pending)}")
    if not pending:
        return 0
    load_dotenv(Path(".env"))
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Configure OPENAI_API_KEY locally in .env before resuming.")
    semaphore = asyncio.Semaphore(workers)
    failures = []
    (audit / "api_responses").mkdir(exist_ok=True)

    async with AsyncOpenAI(timeout=90, max_retries=1) as client:

        async def critique(path: Path) -> None:
            job = json.loads(path.read_text())
            async with semaphore:
                try:
                    response = await client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": job["instruction"]},
                            {"role": "user", "content": json.dumps(job)},
                        ],
                        response_format={"type": "json_object"},
                    )
                    # Preserve the actual response even when its content is invalid.
                    with (audit / 'api_responses' / path.with_suffix('.jsonl').name).open('a') as saved:
                        saved.write(response.model_dump_json() + '\n')
                    result = json.loads(response.choices[0].message.content or "")
                    opening = result["opening_message"]
                    followups = result["followups"]
                    assert isinstance(opening, str) and opening.strip()
                    assert isinstance(followups, list)
                    assert all(isinstance(s, str) and s.strip() for s in followups)
                    assert len(followups) + 1 == job["task"]["turn_count"]
                    assert isinstance(result["issues"], list)
                    assert isinstance(result["changed"], bool)
                    output = audit / "critic" / path.name
                    with output.open("x") as handle:
                        handle.write(json.dumps(result, ensure_ascii=False) + "\n")
                    print(f"Saved critique: {path.stem}", flush=True)
                except Exception as exc:
                    failures.append(path.stem)
                    # Do not print provider exception bodies or credential values.
                    print(f"Pending: {path.stem} ({type(exc).__name__})", flush=True)

        await asyncio.gather(*(critique(path) for path in pending))
    print(f"Batch complete; failed critiques still pending: {len(failures)}")
    return int(bool(failures))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    if args.workers < 2 or (args.limit is not None and args.limit < 1):
        parser.error("Use at least two workers and a positive optional limit.")
    raise SystemExit(asyncio.run(run(args.model, args.workers, args.limit)))


if __name__ == "__main__":
    main()
