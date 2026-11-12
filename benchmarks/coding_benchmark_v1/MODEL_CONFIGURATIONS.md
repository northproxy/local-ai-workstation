# CB01 — Model Configurations

**Project:** Local AI Workstation  
**Recorded:** 2026-11-12  
**Evidence:** LM Studio screenshots shared during model inventory; user's subsequent confirmation that all models were configured and Thinking was disabled.  
**Scope:** Coding Benchmark CB01 (Directory Integrity Scanner). No benchmark score is implied by model size.

## Hardware and measurement boundaries

Windows 11 laptop; AMD Ryzen 9 8940HX, 32 GB system RAM, NVIDIA GeForce RTX 5070 Laptop GPU (8 GB VRAM); inference through LM Studio. LM Studio version, backend/build, actual GPU VRAM use, memory peaks and exact post-configuration offload values have **not** been captured. `TBD` means unverified; `Off` means the setting was visibly disabled or explicitly confirmed. The original screenshot inventory is **not** proof of settings effective for a particular inference request.

## Model identities and loading parameters — initial screenshots

| Field | Qwen3.5-9B | Qwen3-14B | Qwen3.8-27B | Qwen3-8B |
|---|---|---|---|---|
| Model ID / repository | `qwen/qwen3.5-9b` | `lmstudio-community/Qwen3-14B-GGUF` | `lmstudio-community/Qwen3.8-27B-GGUF` **(inferred from truncated UI text; verify)** | `lmstudio-community/Qwen3-8B-GGUF` |
| GGUF filename | `Qwen3.5-9B-Q4_K_M.gguf` | `Qwen3-14B-Q4_K_M.gguf` | `Qwen3.8-27B-Q4_K_M.gguf` | `Qwen3-8B-Q4_K_M.gguf` |
| File size shown | 6.55 GB | 9.00 GB | 17.74 GB | 5.03 GB |
| Quantization | Q4_K_M | Q4_K_M | Q4_K_M | Q4_K_M |
| Architecture shown | `qwen35` | `qwen3` | `qwen35` / `MTP` | `qwen3` |
| Model-supported context shown | 262144 | 32768 | 262144 | 32768 |
| **Initial configured context** | **16384** | **8192** | **16384** | **16384** |
| **Initial GPU Offload setting** | **32** (slider at right end) | **32** | **32** | **32** |
| CPU thread pool | 12 | 12 | 12 | 12 |
| Evaluation batch / physical batch | 2048 / 512 | 2048 / 512 | 2048 / 512 | 2048 / 512 |
| Max concurrent predictions | 4 | 4 | 4 | 4 |
| Unified KV cache | On | On | On | On |
| Context checkpoints | 32 | 32 | 32 | 32 |
| KV cache offload to GPU | On | On | On | On |
| K/V cache quantization | Disabled | Not captured in screenshot | Disabled | Disabled |
| Flash Attention | On | On | On | On |
| Keep model in memory | On | On | On | On |
| Try mmap | On | On | On | On |
| Seed in initial screenshot | Random | Random | Random | Random |
| Speculative decoding | Off | Off | **MTP On** | Off |

For 27B MTP, the screenshot additionally showed `max draft tokens = 2`, `min draft tokens = 0`, `draft probability = 0.75`. An offload slider value of 32 does **not** establish comparable VRAM use or percentages across architectures.

## Initial inference/sampling screenshots

| Field | Qwen3.5-9B | Qwen3-14B | Qwen3.8-27B | Qwen3-8B |
|---|---|---|---|---|
| Temperature | 0.2 | 0.2 | 0.2 | 0.2 |
| Top K | 20 | 20 | 40 | 40 |
| Top P | 0.9 (On) | 0.9 (On) | 0.95 (On) | 0.9 (On) |
| Min P | Off | Off | 0.05 (On) | 0.05 (On) |
| Repeat penalty | Off | Off | 1.1 (On) | 1.1 (On) |
| Presence penalty | 1.5 (On) | Off | Off | Off |
| Thinking in **first screenshot** | On | Off | Not visible (section collapsed) | Not visible (section collapsed) |
| Thinking **later user confirmation** | Off | Off | Off | Off |
| Limit response length in initial screenshot | Off | Off | Off | Off |
| Context overflow in screenshots | Truncate Middle | Truncate Middle | Truncate Middle | Truncate Middle |

**Interpretation:** On 2026-11-12, the user stated that *all models had been configured* and that Thinking was Disabled for all. This establishes the intended user configuration, not a per-request runtime trace. Settings not re-screenshotted after adjustment remain unverified at inference time.

## Agreed main-run target profile (not automatically verified)

| Parameter | Target |
|---|---|
| Context | 16384 tokens |
| Temperature | 0.2 |
| Top K / Top P | 20 / 0.9 |
| Min P / repeat penalty / presence penalty | Disabled |
| Thinking | Disabled |
| Speculative Decoding / MTP | Disabled |
| Flash Attention | Enabled |
| CPU thread pool | 12 |
| Seed | 42 if supported; otherwise record effective seed/random state |
| GPU Offload | Maximum **stable** for each model, record actual layers and memory use; don't force equal numbers |
| Desired response cap | 8192 output tokens, **NOT VERIFIED** in LM Studio Chat; UI rejected values above 2048 |
| Context overflow policy | Prefer Stop at Limit; **not verified** as applied for Run01 |

The 8192 cap cannot be marked active merely because it was proposed. The user established that the Chat UI did not accept values above 2048. A future local-API test may establish whether a longer cap is available **in that route and model/runtime**. Do not silently treat Chat and API runs as the same protocol.

## Snapshot-to-run audit checklist

For each actual run, fill the effective values **after model load**, not only the saved UI defaults:

```
Run ID:
LM Studio version / engine build / endpoint (Chat or API):
Model ID / GGUF / quantization:
Context / GPU offload / VRAM idle, loaded, peak / RAM idle, loaded, peak:
Thinking state / MTP state / chat template (if verifiable):
Temperature / top_k / top_p / min_p / repeat / presence / seed:
Output token cap / overflow behavior:
Prompt hash verified? / prompt tokens / generated tokens:
TTFT / generation seconds / tok/s / total wall time / stop reason:
Output archived / code extracted / tests run / manual edits:
Unverified values and deviations:
```

See `BENCHMARK_PROTOCOL.md`, `KNOWN_ISSUES.md` and existing `CB01_Qwen3.5-9B_Run01.md`.
