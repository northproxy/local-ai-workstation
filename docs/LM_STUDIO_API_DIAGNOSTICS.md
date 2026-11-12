# LM Studio — Local API Diagnostics

**Project:** Local AI Workstation  
**Date:** 2026-11-12  
**Status:** API smoke tests passed; official CB01 rerun not performed  
**Intended repository path:** `docs/LM_STUDIO_API_DIAGNOSTICS.md`  
**Evidence:** User-provided PowerShell outputs, LM Studio screenshots, two preset JSON files, and existing CB01 documentation.  
**GitHub status:** Draft only — not committed or pushed.

## 1. Purpose

Inventory LM Studio and verify whether its Native REST API offers reproducible, bounded local generation independent of the Chat UI's observed response-length validator. These are diagnostic tests, **not** official Coding Benchmark CB01 results.

## 2. Environment and inventory

| Field | Observation | Evidence / qualification |
|---|---|---|
| OS / CPU / RAM | Windows 11 / Ryzen 9 8940HX / 32 GB | Project inventory |
| GPU | RTX 5070 Laptop, 8 GB VRAM | Project inventory |
| LM Studio before update | 0.4.21 (Build 2), Stable | GUI screenshot |
| LM Studio after update | Updated; believed to be 0.4.28 (Build 2) | User confirmed update; **exact version/build not independently recaptured** |
| Selected runtime at initial inventory | `llama.cpp-win-x86_64-nvidia-cuda12-avx2@2.73.0` | `lms runtime ls` **before update**; post-update runtime TBD |
| API base URL | `http://127.0.0.1:1234` | Successful loopback HTTP requests |
| Model ID | `qwen/qwen3.5-9b` | CLI and API |
| Format / quantization | GGUF / Q4_K_M | `lms ps --json` |
| Loaded context | 16384 | CLI and Native API |
| Supported context | 262144 | CLI and Native API |

`lms ls` showed five LLMs (`qwen/qwen3.5-9b`, `qwen3-14b`, `qwen3.8-27b`, `qwen3-8b`, `gemma-4-e4b-it-qat`) and one embedding model (`text-embedding-nomic-embed-text-v1.5`), 44.55 GB total on disk. **Installed does not mean loaded.**

## 3. API discovery and runtime configuration

### `GET /v1/models` — PASS

Returned six available model IDs. This confirms OpenAI-compatible local API reachability, not six resident models.

### `GET /api/v1/models` — PASS

A user-provided excerpt for the loaded `qwen/qwen3.5-9b` instance reported:

```json
{
  "context_length": 16384,
  "eval_batch_size": 2048,
  "physical_batch_size": 512,
  "parallel": 4,
  "flash_attention": true,
  "lazy_mode": "auto",
  "context_checkpoints": 32,
  "reasoning_budget_message": "",
  "speculative_draft_mtp": false,
  "speculative_draft_simple": false,
  "speculative_draft_model": "",
  "speculative_draft_max_tokens": 3,
  "speculative_draft_min_tokens": 0,
  "speculative_draft_min_continue_probability": 0,
  "offload_kv_cache_to_gpu": true
}
```

API also reported `max_context_length: 262144` and `format: gguf`. These fields describe the loaded instance; they do **not** verify the actual GPU offloaded layers, peak VRAM/RAM, Chat template, or the sampling parameters of historical CB01 Run01. Empty `reasoning_budget_message` is **not proof** of Thinking being off.

## 4. Native inference smoke tests

**Endpoint:** `POST /api/v1/chat`  
**Model:** `qwen/qwen3.5-9b`  
**Shared request parameters:** `reasoning="off"`, `temperature=0.2`, `top_k=20`, `top_p=0.9`, `stream=false`, `store=false`.

### Short coding request — PASS

Prompt: `Write a Python function add(a, b) that returns the sum of two numbers. Return only executable Python code.`

| `max_output_tokens` | Input tokens | Output tokens | Reasoning tokens | tok/s | TTFT (s) |
|---:|---:|---:|---:|---:|---:|
| 256 | 35 | 18 | 0 | 56.8646 | 0.267434 |
| 4096 | 35 | 18 | 0 | 55.8836 | 0.174807 |
| 8192 | 35 | 18 | 0 | 56.3356 | 0.181326 |

All requests returned the same correct function, surrounded by Markdown code fences:

```python
def add(a, b):
    return a + b
```

**Interpretation:** The Native API accepted caps of 4096 and 8192 and completed short generations. This does **not** prove that 8192 output tokens can be generated or that the cap is enforced at 8192. Markdown fences are a minor deviation from the literal "only executable Python code" request.

### Long-output diagnostic — PASS for generation >2048 tokens

Prompt: `Generate 350 numbered lines. Each line must contain its number followed by exactly these words: red green blue orange purple silver gold copper. Do not add explanations.`

`max_output_tokens=3072`, all other parameters unchanged.

| Metric | Measured |
|---|---:|
| Input tokens | 46 |
| Total output tokens | **3072** |
| Reasoning output tokens | 0 |
| Tokens per second | 47.1270 |
| TTFT | 0.302278 s |
| Last displayed numbered line | 265 |
| Requested numbered lines | 350 |

The returned answer began with correctly numbered lines and its captured tail ended at line 265. **The 350-line task was not completed.** Exactly 3072 tokens were reported, matching the requested cap; however, **no explicit stop-reason value was provided**, so do not claim that the termination reason itself was verified. Repetition in this particular response was required by the prompt, unlike the CB01 planning loop.

**Established:** Native API can generate **more than 2048 output tokens** on this machine with this model and route. This disproves an API/engine-wide 2048 output-token ceiling for the tested route.

## 5. Chat UI and preset observations

- Chat UI previously rejected `Limit Response Length` values above 2048; a later Chat retry reported **2048 output tokens** with visible stop reason `Max Predicted Tokens Reached`, without complete CB01 code. This is a **GUI-specific observation**, not an API-wide limitation.
- Two user-provided preset JSON files (`test_Qwen3-14B-GGUF` and `LAIW_inventory_test`) contained only `llm.prediction.reasoning.enableThinking: true` under `operation.fields`, with `load.fields: []`.
- The user reported **Thinking Disabled** in the GUI. Preset file contents do **not** establish effective reasoning behavior of a generation. Neither preset constitutes a complete backup of load and inference settings.
- Keep safe, explicit project-side configuration manifests rather than relying on undocumented LM Studio internal state. Do not commit secrets, model weights, caches, machine-specific paths, or private prompts.

## 6. Relationship to CB01

Historical `CB01-Qwen3.5-9B-Run01` is unchanged: **15589 output tokens**, **44.02 tok/s**, **354.66 s processing**, `truncated=1` near the 16384 context boundary; repeated planning, no complete `integrity.py` or `test_integrity.py`, automated tests **not run**. A subsequent Chat UI retry also did not finish the coding task under its 2048-token cap.

The API successfully generated a *much simpler* `add(a, b)` function. Because the **task and transport both changed**, this cannot establish that Native API resolves CB01 looping or that Qwen3.5-9B can complete the frozen CB01 prompt. No new official CB01 result or comparative model score is implied.

## 7. Verified, unresolved, and next actions

**Verified:** both model-list endpoints respond on loopback; Qwen3.5-9B generates short code via Native API; requests with caps 4096/8192 are accepted; a 3072-token response was generated; API stats reported 0 separately counted reasoning tokens for these `reasoning="off"` tests.

**Unresolved:** exact post-update LM Studio and runtime builds, per-run GPU placement and memory peaks, effective CB01 template/reasoning, explicit long-output finish reason, full 8192-token capacity, and root cause of CB01 looping.

**Next actions (in order):**

1. Capture **post-update** version/build and `lms runtime ls`; keep the earlier inventory as historical evidence.
2. Preserve this diagnostic report and avoid changing CB01 Run01 history.
3. Freeze a minimal Native API CB01 protocol using the exact existing prompt/hash, explicit request settings, stable loaded configuration, raw output + stats + wall time, timeout/errors, and a fresh Run ID.
4. Determine available stop/finish reporting before interpreting capped official runs.
5. Only after one stable protocol, compare candidate models fairly. Python automation and Open WebUI come later.

### Safe read-only inspection (PowerShell)

```powershell
lms runtime ls
lms ps --json
lms server status --json --quiet

Invoke-RestMethod -Uri "http://127.0.0.1:1234/v1/models" -Method Get |
    ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://127.0.0.1:1234/api/v1/models" -Method Get |
    ConvertTo-Json -Depth 15
```

Keep `Serve on Local Network` off; never expose this local server to the public internet.

## References

- [LM Studio developer documentation](https://lmstudio.ai/docs/developer)
- [LM Studio REST API documentation](https://lmstudio.ai/docs/developer/rest)
- Repository: `northproxy/local-ai-workstation`, branch `main`
- `PROJECT.md`
- `benchmarks/coding_benchmark_v1/MODEL_CONFIGURATIONS.md`
- `benchmarks/coding_benchmark_v1/KNOWN_ISSUES.md`
- `benchmarks/coding_benchmark_v1/BENCHMARK_PROTOCOL.md`
