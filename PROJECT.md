# PROJECT — Local AI Workstation

## Mission

Build a local AI platform that supports other projects.

The system should gradually provide:

- local LLM inference;
- a local OpenAI-compatible API;
- an ergonomic chat UI;
- project/file access through controlled tools;
- coding assistance;
- RAG over project documentation;
- a second AI node on the desktop PC;
- automation;
- agents where they provide a measurable benefit.

## Current status

The laptop is already capable of running local models through LM Studio.

### Measured results

| Model | Result |
|---|---|
| Gemma 4 E4B QAT | ~52 tok/s |
| Qwen3-14B Q4_K_M | ~8.5 tok/s |
| Qwen3.8-27B Q4 | ~0.7 tok/s |
| Qwen3.5-9B | ~43–45 tok/s on Core T01–T05; TTFT ~0.3–0.5 s |

Subjectively, Qwen3-14B produces more satisfying answers than the much faster Gemma. Qwen3.5-9B is now a strong interactive-speed candidate, but its benchmark quality scoring is not complete yet.

This establishes an important project rule:

> Model selection should optimize useful answer quality at acceptable latency, not raw generation speed alone.

## Immediate next step

**Active milestone (2026-11-12):** verify the LM Studio local API and a reliable bounded-output execution route for **Coding Benchmark CB01**, then compare four local models using an unchanged prompt and one controlled run protocol.

The earlier Qwen3.5-9B Core Benchmark T01–T05 is still awaiting full metadata recovery and quality scoring; this work remains open and should not be mistaken for the new CB01 coding experiment. The preferred daily model has **not** yet been selected.

### Coding Benchmark CB01 — current status (2026-11-12)

- Task: **Directory Integrity Scanner** (Python 3.11+ CLI; model-generated `integrity.py` and `test_integrity.py`).
- Candidate inventory complete from LM Studio screenshots: Qwen3.5-9B, Qwen3-14B, Qwen3.8-27B, Qwen3-8B; all Q4_K_M GGUF. User reports all models configured and Thinking disabled.
- Frozen prompt, rubric (60 automated + 40 expert points), evaluation program and results template prepared under `benchmarks/coding_benchmark_v1/`.
- `CB01-Qwen3.5-9B-Run01` on 2026-11-12: **15589 output tokens, 44.02 tok/s, 354.66 s runtime processing, `truncated = 1`**. Repetitive planning; no complete Python code delivered; **automated tests not run**. The failure is recorded without declaring a model winner or a full /100 score.
- LM Studio Chat `Limit Response Length` UI was observed to reject values above **2048**, so the intended 8192 output-token cap was **not verified** for Run01.
- Next: confirm current LM Studio build and local API capabilities, verify output cap and thinking/template handling with a diagnostic prompt, then freeze the comparison transport and rerun as needed. Keep Run01 unchanged in history.

See `benchmarks/coding_benchmark_v1/MODEL_CONFIGURATIONS.md`, `BENCHMARK_PROTOCOL.md`, `KNOWN_ISSUES.md`, and the original Run01 report.

## Near-term milestone

After selecting the primary model:

1. Start the LM Studio local server.
2. Verify `/v1/models`.
3. Make a local API call from Python.
4. Connect Open WebUI.
5. Add restricted filesystem/Git tooling.
6. Test the system on one real software project.

## Second machine

A desktop computer with an older 8 GB GPU is available.

Do not assume it should be used for distributed inference.

Preferred first approach:

- laptop = main interactive/reasoning/coding model;
- desktop = independent utility workload.

Possible desktop roles:

- embeddings;
- RAG indexing;
- smaller utility LLM;
- summarization/classification;
- background processing;
- automation worker.

Final role depends on exact GPU, CPU and RAM.

## Security baseline

Before enabling agents or MCP tools:

- use trusted MCP servers only;
- scope filesystem access to explicit project folders;
- avoid unrestricted shell execution;
- never expose the local inference server to the public internet by default;
- keep secrets in `.env` or OS credential storage;
- keep `.env` excluded from Git;
- review write/delete actions;
- prefer Git-tracked workspaces so changes can be inspected and reverted.

## Not in scope yet

Avoid premature complexity:

- Kubernetes;
- distributed multi-GPU inference over LAN;
- large multi-agent teams;
- custom vector databases before RAG is actually needed;
- fine-tuning before good prompting/RAG/tooling has been exhausted.

## Success criteria for v1

The project reaches v1 when:

- a preferred local model is selected;
- laptop and desktop roles are defined;
- local API is stable;
- one unified UI works;
- the AI can safely inspect selected project files;
- it can assist with Git/code tasks;
- it can retrieve relevant project knowledge;
- at least one real existing project is materially easier to maintain with the system.
