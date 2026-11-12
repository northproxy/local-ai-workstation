# CB01 — Evaluation and run protocol (v1.0)

## Objective
Compare Qwen3.5-9B, Qwen3-14B, Qwen3.8-27B and Qwen3-8B on identical Python engineering work, not model size. Scores are not assigned until submitted code is run.

## Score: 100 points

### Automated behavioral tests: 60 points
12 independent tests at 5 points each, using `evaluate.py`. Binary per test: pass 5, fail 0. A skipped test scores 0 and must be explained.

1. Snapshot: correct nested/hidden/binary/empty file manifest, checks file sizes and SHA-256.
2. Snapshot reproducibility: identical contents yield byte-identical JSON.
3. Compare unchanged: exact JSON lists and exit 0.
4. Compare changed: added/modified/deleted sorted and exit 1.
5. Same-size content edit recognized by hash.
6. Missing ROOT: exit 2, stderr, no traceback/no stdout JSON.
7. Invalid baseline JSON: exit 2, stderr, no stdout JSON.
8. Invalid baseline schema: exit 2 (multiple malformed structures).
9. Manifest location inside ROOT rejected for both commands.
10. Nonexistent output parent created; snapshot succeeds.
11. Unicode paths preserved and compared correctly.
12. Symlinks are ignored without following (skip only when OS permissions prevent creation; mark as untested, no 5 points until rerun on a symlink-capable environment).

### Expert evaluation: 40 points, separately reported
- Architecture / maintainability (0–12): separation of concerns, naming, clarity, reasonable modularity.
- Model-written test quality (0–12): meaningful coverage and assertions, executable tests, no hard-coded local paths.
- Safety / reliability (0–8): failure-atomic snapshot writes, meaningful errors, no unexpected mutation, careful file handling.
- Instruction compliance (0–8): output format, standard-library only, complete files, Python 3.11+, no major spec omissions.

Score each expert subcategory with evidence; do not make up scores for missing artifacts. Report `automated/60`, `expert/40`, and `total/100` separately. Note that the atomic-write behavior is also inspected manually, not fully proved by the automated suite. Record manual intervention and whether original code or patched code was tested; the official score must use original code.

## Runtime protocol
- Same Windows 11 laptop, same installed LM Studio version, same benchmark prompt, fresh empty chat per model.
- Record exact model ID, GGUF filename and quantization, context, GPU offload (layers or %), Flash Attention, KV-cache settings, thinking state, temperature, top-p, top-k, min-p, repeat penalty, seed, max tokens and runtime/backend. Use `N/A` if unavailable, `TBD` only if not yet checked.
- Proposed common settings, **subject to compatibility verification before first run**: context 16384; max output 8192; temperature 0.2; top-p 0.9; other sampling settings fixed to LM Studio defaults and recorded. Do not silently force settings that a model does not support.
- Main comparison: thinking disabled for every model only if equivalent disable control exists for all; otherwise document per-model thinking and do not claim strict like-for-like reasoning comparison. Optional thinking ON is a *separate* experiment, not mixed into main ranking.
- Apply same GPU offload **policy** (maximum stable offload without out-of-memory errors, same background workload), not identical offload layer count. Record actual values. The large model may use far more system RAM; interpret results accordingly.
- Before each run: close other models, preserve power mode/charger state, leave similar background load, open new empty chat, paste the frozen English prompt, start timing. Do not let the model use external tools.
- Collect: prompt tokens, output tokens (including reasoning tokens if reported), TTFT, prompt processing time, generation tok/s, generation duration, total elapsed wall time, stop reason, RAM, VRAM. If LM Studio does not expose a metric, mark `not available` and use a separate wall clock if feasible.
- TTFT = time from request submission to first visible generated token (if measured); total = request submission to completed response. Generation tokens/sec is not quality score.
- Do not edit prompt between models. If a model truncates due to token limit, record truncation; do not give extra continuation for official first-pass score. Optional repaired runs are separate.
- Capture exact raw response before extracting source files; do not repair formatting or errors for the official evaluation.

## Candidate identities
| Model | GGUF size supplied | Exact GGUF file | Quant | Context | Offload | Thinking |
|---|---:|---|---|---|---|---|
| Qwen3.5-9B | 6.5 GB | TBD | TBD | TBD | TBD | TBD |
| Qwen3-14B | 9.0 GB | TBD | previously Q4_K_M, verify | TBD | TBD | TBD |
| Qwen3.8-27B | 17.7 GB | TBD | previously Q4, verify exact variant | TBD | TBD | TBD |
| Qwen3-8B | 5.0 GB | TBD | TBD | TBD | TBD | TBD |

## Results template
For each model, fill:
```
Model:
GGUF filename / repository / quantization:
LM Studio version / backend:
Context / GPU offload / Flash Attention / KV cache:
Thinking Enabled/Disabled / temperature / top-p / top-k / min-p / repeat penalty / seed:
Max output tokens:
VRAM before / after load / peak:
RAM before / after load / peak:
Prompt tokens / output tokens:
TTFT / prompt processing seconds / generation seconds / total wall seconds / tok/s:
Stop reason:
Raw response archived at:
Original files extracted without modifications? YES/NO:
Run command / Python version / OS:
Automated: __ / 60 ; tests passed __ / 12 ; skipped __
Expert architecture __/12 ; generated tests __/12 ; safety __/8 ; instruction compliance __/8
Expert subtotal __ /40 ; overall __ /100
Manual edits needed (not included in score):
Problems / edge cases / security issues:
Daily-use assessment (separate qualitative judgment):
```
