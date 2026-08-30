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

Subjectively, Qwen3-14B produces more satisfying answers than the much faster Gemma.

This establishes an important project rule:

> Model selection should optimize useful answer quality at acceptable latency, not raw generation speed alone.

## Immediate next step

Benchmark **Qwen3.5-9B** in LM Studio.

Record:

- exact model/repository;
- quantization;
- context length;
- GPU offload;
- VRAM usage;
- RAM usage;
- tokens/sec;
- time to first token;
- subjective quality.

Then compare it directly with Qwen3-14B using identical prompts.

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
