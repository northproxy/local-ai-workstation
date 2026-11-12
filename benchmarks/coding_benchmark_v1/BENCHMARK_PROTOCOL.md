# CB01 — Benchmark Execution Protocol

**Version:** 1.0 (operational addendum, 2026-11-12)  
**Project:** Local AI Workstation  
**Task:** Directory Integrity Scanner — Python 3.11+ CLI  
**Participants:** Qwen3.5-9B, Qwen3-14B, Qwen3.8-27B, Qwen3-8B.

## Authoritative files and immutability

- `PROMPT_EN.md` contains the **frozen English task**. Paste *only* the delimited prompt content. Do not rewrite, abbreviate, add a postscript, or supply hints to individual models.
- `PROMPT_SHA256.txt` is the stored integrity check. Verify against **the same exact bytes/span whose hash was originally recorded**; never invent a replacement hash or change the prompt without a new version.
- `RUBRIC_AND_PROTOCOL.md` is the authoritative scoring rubric: 12 automated checks × 5 points (60), plus architecture 12, model-written tests 12, safety 8, instruction following 8 (40). This file complements, rather than replaces, that rubric.
- `evaluate.py` is the prepared evaluator. Keep the evaluator version/hash fixed for the four-run comparison. If evaluator bugs need fixing, record evaluator versions and rerun all available solutions under the same corrected version.
- `RESULTS.csv` is the comparison ledger. Do not award a test pass without executing it.

## Fairness rules

1. Same Windows 11 laptop (Ryzen 9 8940HX, 32 GB RAM, RTX 5070 Laptop 8 GB VRAM), Python version, LM Studio version/engine whenever possible, AC power/performance mode, background load policy and input prompt.
2. One model loaded at a time; fresh chat/request context for each run. No external tools or network assistance to the generation; do not supply feedback before the official initial submission.
3. Use the common target sampling/context settings in `MODEL_CONFIGURATIONS.md` **only if verified effective**. Thinking disabled; MTP disabled; temperature 0.2; top_k 20; top_p 0.9; min_p, repeat and presence penalties disabled; Flash Attention enabled.
4. GPU Offload is hardware-adaptive: use the maximum stable allocation for that model; record actual layer count and VRAM/RAM use. Equal Offload numbers are not required or proof of equivalent compute placement.
5. Record deviations before comparing performance. If a model cannot use the agreed context/output policy, keep its result but mark the configuration difference prominently. Do not pretend the comparison is strictly controlled.
6. Preserve raw response (including reasoning text, if exposed) before extracting code. Do not correct model output to improve the official first-pass score. A repaired or repeated attempt has a new Run ID.
7. Do not continue a truncated answer in the official pass. Keep any diagnostic follow-up separate from the original.
8. Report automatic test results, expert score, manual fixes and practical usefulness **separately**. Never infer code quality from tokens/second.

## Output length and context overflow — current blocker

The agreed *target* was context 16384 and output limit 8192. In the Windows LM Studio Chat UI the user verified that `Limit Response Length` rejected values greater than **2048** (red validation outline); consequently 8192 has **not** been established as an effective Chat limit. In Qwen3.5-9B Run01, the runtime log reported 15589 generated tokens with `truncated = 1`, consistent with reaching its 16384-token slot boundary, **not** with an enforced 8192-token output cap. The user-visible `Thinking Disabled` setting does not establish whether internal reasoning text was disabled in that request: the archived response included a `Thinking Process:` section. See `KNOWN_ISSUES.md`.

**Hold point before the next official run:**

1. Start LM Studio local server on loopback only (e.g., `localhost:1234`) and verify an endpoint and exact loaded model ID; do not expose it publicly.
2. Run a **short, separate diagnostics prompt** to confirm the chosen API route, effective response-token cap, and stop reporting. A request parameter such as `max_tokens` or `max_output_tokens` depends on the API endpoint: inspect the current LM Studio API implementation; do not assume UI limits or parameter support transfer across endpoints.
3. Verify the model does not emit or consume uncontrolled long reasoning when Thinking is intended Off. Capture the effective chat template/behavior if possible.
4. Freeze the new transport, token-cap policy, overflow mode, request template and measurements **before** testing the remaining models. If transport or protocol changes, label the sequence a new comparison cohort and rerun any models required for fair comparison.

Changing `Context Overflow` from `Truncate Middle` to `Stop at Limit` is a recommended diagnostic/safety policy, **not retroactively the Run01 setting**. Context overflow behavior and maximum response length are distinct controls.

## Procedure for a controlled attempt

**Before request:** capture model ID, GGUF, quantization, LM Studio/engine, OS and Python, context length, GPU offload, KV-cache/Flash Attention, sampling, Thinking, MTP, response cap, overflow mode, API/Chat route, RAM/VRAM after loading, and prompt hash. Use `TBD` where not measured.

**Generate:** send the frozen prompt once. Record submit time, first-token time (if measured), prompt tokens, output tokens (reasoning and visible segments if available), processing duration, generation duration, total wall-clock duration, tok/s, stop reason and any truncation/overflow warnings. Avoid mixing metrics from follow-up internal tasks with the main request.

**Archive:** save complete raw text, unmodified logs, settings, exact extracted `integrity.py`/`test_integrity.py` if present, hashes and a concise run report. Never paste non-existent code into scoreable files.

**Evaluate:** run the pinned `evaluate.py` against only the unmodified generated program in a controlled temporary working folder and record test-by-test results. Run the model's `unittest` suite separately. Respect Windows symlink privilege differences and report skips explicitly, not as passes. Perform evidence-based expert review and report `automated/60`, `expert/40`, `total/100` only when applicable.

**Compare:** maintain separate rankings for correctness, speed, latency, memory footprint, and daily-use quality. If a run has no executable artifact, record `not run` for tests (and an explicit `no executable solution` zero credit as a classification if using the ledger); do not label 12 unexecuted tests as executed failures.

## Recorded run baseline — Qwen3.5-9B Run01

| Metric | Value |
|---|---|
| Date and Run ID | 2026-11-12 / `CB01-Qwen3.5-9B-Run01` |
| Model | `qwen/qwen3.5-9b`; `Qwen3.5-9B-Q4_K_M.gguf` |
| Prompt tokens reported | 795 |
| Output tokens reported | 15589 |
| Prompt eval | 581.68 ms |
| Generation | 354081.92 ms |
| Runtime total | 354663.60 ms |
| Generation throughput | 44.02 tok/s |
| Context / termination | 16384, `truncated = 1` |
| TTFT, VRAM/RAM peak, LM Studio build | Not measured |
| Answer | Repetitive planning; no complete `integrity.py` or `test_integrity.py` |
| Automated tests | Not run — no executable program |
| Score | Do not calculate full /100. Earlier `0/60` was *no artifact credit*, not 12 test failures. |

A second short task appeared in the log after the main task (76 prompt tokens, 9 generated). Its purpose was not established and its metrics are excluded from the main-run totals. The raw response recorded repeated `Wait:` segments; this is evidence of repetition, not a definitive root-cause diagnosis.

## Naming and storage

Use `CB01-<model>-RunNN` for individual requests and preserve any protocol changes in a run-specific metadata note. Recommended location: `benchmarks/coding_benchmark_v1/runs/<model>/runNN/`, or retain the already committed Run01 report in the benchmark root and add references without moving history arbitrarily. Avoid committing secrets, local API credentials, model weights, personal absolute paths or runtime caches.
