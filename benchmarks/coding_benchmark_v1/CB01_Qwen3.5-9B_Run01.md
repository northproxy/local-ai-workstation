# CB01 — Qwen3.5-9B — Run01

**Project:** Local AI Workstation  
**Benchmark:** CB01, Directory Integrity Scanner  
**Date:** 2026-11-12  
**Run ID:** `CB01-Qwen3.5-9B-Run01`  
**Classification:** Initial official attempt; incomplete output / context truncation  
**Status:** Archived; no code available for execution

## 1. Purpose and fixed task

The model was asked to produce a small Python 3.11+ CLI application for directory integrity snapshots and comparisons, plus its own `unittest` suite. The frozen English specification requires two complete files, `integrity.py` and `test_integrity.py`, with no third-party libraries. The main requirements cover SHA-256 hashing, recursive traversal without following symbolic links, deterministic and atomic manifest writing, strict baseline validation, predictable JSON comparison output, and documented exit codes.

**Prompt source:** `PROMPT_EN.md` (CB01 v1.0). The precise prompt bytes/hash were not independently reconstructed from the LM Studio request log; do not treat the archived displayed text as proof of exact prompt bytes.

## 2. Hardware and model identity

| Field | Recorded value | Basis |
|---|---|---|
| OS | Windows 11 | Project hardware inventory |
| CPU | AMD Ryzen 9 8940HX | Project hardware inventory |
| System RAM | 32 GB | Project hardware inventory |
| GPU | NVIDIA RTX 5070 Laptop GPU | Project hardware inventory |
| VRAM capacity | 8 GB | Project hardware inventory |
| Model | `qwen/qwen3.5-9b` | LM Studio Info screenshot |
| GGUF file | `Qwen3.5-9B-Q4_K_M.gguf` | LM Studio Info screenshot |
| Quantization | `Q4_K_M` | LM Studio Info screenshot |
| On-disk size | 6.55 GB | LM Studio Info screenshot |
| Architecture | `qwen35` | LM Studio Info screenshot |
| LM Studio version | Not recorded | — |
| Runtime/backend version | Not recorded | — |

## 3. Runtime configuration

Settings were collected from screenshots during inventory and user confirmation before the benchmark. **Some settings were not independently captured at request submission, so their effective values remain to be verified.**

| Field | Recorded / reported |
|---|---|
| Context length | 16,384 tokens |
| GPU offload | 32 (LM Studio displayed value; actual VRAM use unrecorded) |
| CPU thread pool | 12 |
| Evaluation batch size | 2048 |
| Physical batch size | 512 |
| Unified KV cache | Enabled |
| KV cache offload to GPU | Enabled |
| K/V cache quantization | Not enabled |
| Flash Attention | Enabled |
| Speculative decoding | Off |
| Temperature | 0.2 |
| Top K | 20 in initial screenshot |
| Top P | 0.9 in initial screenshot |
| Min P | Disabled in initial screenshot |
| Repeat penalty | Disabled in initial screenshot |
| Presence penalty | Initially 1.5; user later reported all models configured, but effective Run01 value not separately verified |
| Thinking | Reported Disabled by user; emitted output nevertheless contains `Thinking Process:` |
| Reasoning budget | Not independently verified at run time |
| Seed | Initially random; effective Run01 value not independently verified |
| Maximum response length | Intended 8192; **not proven active**. LM Studio UI was later observed to reject values above 2048. |
| Context overflow mode | `Truncate Middle` shown in post-run screenshot; effective mode at Run01 not independently verified |
| GPU VRAM used / peak | Not measured |
| System RAM used / peak | Not measured |

## 4. LM Studio log measurements

The following values come from the **main generation task, task 0**, ending at local timestamp **2026-11-12 18:50:09**:

| Metric | Value |
|---|---:|
| Prompt processing | 795 tokens |
| Prompt evaluation duration | 581.68 ms |
| Prompt processing throughput | 1366.73 tok/s |
| Generated tokens | 15,589 |
| Generation duration | 354,081.92 ms (354.082 s) |
| Generation throughput | **44.02 tok/s** |
| Total processing time reported by runtime | **354,663.60 ms (354.664 s)** |
| Effective slot token limit / usage | 16,384 / 16,383 reported on release |
| Truncated flag | **1** |
| Time to first visible token (TTFT) | Not measured |
| Stop reason (precise semantic label) | Not separately provided; runtime reports `truncated = 1` |

Selected original log lines:

```text
2026-11-12 18:50:09 [DEBUG]
... prompt eval time =     581.68 ms /   795 tokens (0.73 ms per token, 1366.73 tokens per second)
...        eval time =  354081.92 ms / 15589 tokens (22.72 ms per token, 44.02 tokens per second)
...       total time =  354663.60 ms / 16384 tokens
... slot release: id 0 | task 0 | stop processing: n_tokens = 16383, truncated = 1
```

**Separate post-run task:** the log also includes `task 15593`, with 76 prompt tokens, 9 generated tokens, and total time 376.97 ms. Its purpose is unknown. These measurements are **not** added to the main benchmark generation metrics.

**Time-label clarification:** the 354.664 s figure is the runtime's logged processing total, not an independently timed UI wall-clock duration. The log does not independently establish TTFT.

## 5. Observed response

The supplied LM Studio text export (`Run01_raw_response.txt`) contains a lengthy `Thinking Process:` section followed by repeated self-reminders about requirements, including the manifest location restriction, compare JSON format, error exit code, and stderr handling.

- The archived text includes **808 occurrences** of `Wait:`.
- It contains **zero Markdown code fences**.
- There are no complete `integrity.py` or `test_integrity.py` deliverables in the submitted text.
- The archived response ends mid-sentence.
- The uploaded text begins with the tail of the prompt, then the model header and response. It is a UI text capture, not a structured request/response dump.

**Directly observable outcome:** the main generation reached the context limit (`truncated = 1`) without delivering executable Python files. This is a benchmark failure to produce the requested artifacts, regardless of the high throughput.

## 6. Evaluation — keep automatic and expert assessments separate

| Category | Result | Explanation |
|---|---|---|
| Files extracted unmodified | **No** | Required source files absent |
| Automated suite executed | **No** | No runnable implementation to test |
| Automated test results | **0/12 executed** | Not equivalent to 12 executed failures |
| Automated score | **0/60 deliverable-based provisional score** | No code can satisfy test assertions; not a measured pass/fail run |
| Expert architecture (0–12) | N/A | No implementation |
| Expert model-written tests (0–12) | N/A | No tests delivered |
| Expert safety/reliability (0–8) | N/A | No implementation to inspect |
| Expert instruction following (0–8) | N/A pending rubric decision | Clear non-delivery, but no fabricated numeric expert score |
| Expert subtotal | N/A | Not scored |
| Final total (/100) | **N/A** | Do not present an unmeasured expert score as a full evaluation |
| Manual fixes | None | Official first attempt remains unchanged |

**Outcome label:** `INCOMPLETE_OUTPUT_CONTEXT_TRUNCATION`.

## 7. Interpretation and limitations

**Established:** the model generated approximately 15.6k tokens at 44.02 tok/s, the runtime reported `truncated = 1`, and the archived response has no completed implementation. Repeated planning dominated the output.

**Not established:** whether the UI truly disabled internal thinking for the request; whether `Limit Response Length = 8192` was effective; which sampler settings were actually applied at submission; whether the cause is primarily model behavior, chat-template configuration, or LM Studio inference/runtime behavior. The presence of the text `Thinking Process:` is suggestive but not decisive.

A subsequent check showed the LM Studio `Limit Response Length` field rejects values above **2048** in the user's interface. This was observed **after** Run01 and should not be retroactively treated as a proven Run01 limit.

Do not use generation speed alone to rank coding quality.

## 8. Planned next action

1. Preserve Run01 unchanged and label any further attempt `Run02`.
2. Verify actual sampling, thinking control, max-output-token handling, and the chosen chat template.
3. Consider an LM Studio local API invocation after confirming how its output cap works, without changing CB01 prompt content.
4. Before comparing scores across models, adopt one reproducible run protocol, record all deviations, and retain the original output for every model.
5. Run the same frozen prompt in a fresh conversation; do not append `Continue` to Run01 as an official result.

## 9. Provenance and attachments

- `Run01_raw_response.txt`: original user-supplied text export, saved without editing.
- `Run01_runtime_log.txt`: log excerpt supplied by the user, transcribed as received in the chat.
- `CB01_Qwen3.5-9B_Run01.md`: this report.
- Frozen prompt and benchmark rubric were separately prepared as `PROMPT_EN.md` and `RUBRIC_AND_PROTOCOL.md`.

**GitHub suggestion:** place this report under `benchmarks/cb01/runs/qwen3.5-9b/run01/`. Keep original artifacts alongside it. No repository modifications have been performed as part of creating this report.
