# Local AI Workstation

Локальная AI-инфраструктура для работы с LLM, RAG, MCP, coding agents и автоматизацией.

Главная цель проекта — не просто запускать локальные модели, а создать на собственном железе AI-среду, которая помогает вести другие проекты.

## Hardware

### Laptop
- CPU: AMD Ryzen 9 8940HX with Radeon Graphics
- RAM: 32 GB
- GPU: NVIDIA GeForce RTX 5070 Laptop GPU
- VRAM: 8 GB
- SSD free space at project start: ~300 GB

### Desktop
Характеристики будут добавлены после проверки.

Планируемая роль: второй AI node для отдельной модели, embeddings, RAG или фоновых задач.

## Current software

- Windows
- LM Studio
- Git
- GitHub mirror planned

## Current model benchmarks

| Model | Quantization | Approx. speed | Notes |
|---|---|---:|---|
| Gemma 4 E4B QAT | QAT | ~52 tok/s | Very fast, answer quality less preferred |
| Qwen3-14B | Q4_K_M | ~8.5 tok/s | Current quality/speed baseline |
| Qwen3.8-27B | Q4 | ~0.7 tok/s | Works, but too slow interactively |
| Qwen3.5-9B | TBD | TBD | Next planned test |

## Target architecture

```text
                    LOCAL AI WORKSTATION
                           │
             ┌─────────────┴─────────────┐
             │                           │
          Laptop                      Desktop
     RTX 5070 8 GB                  GPU 8 GB
             │                           │
       Primary LLM                 Utility LLM
       Coding / Chat              Embeddings/RAG
             │                           │
             └─────────────┬─────────────┘
                           │
                      Local network
                           │
                 ┌─────────┴─────────┐
                 │                   │
             Open WebUI          Local APIs
                 │                   │
             MCP / Tools          Automations
                 │
        ┌────────┼─────────┐
        │        │         │
      Files     Git      Shell
        │
     Projects
```

## Roadmap

### v0.1 — Local inference
- [x] Install LM Studio
- [x] Validate NVIDIA GPU inference
- [x] Benchmark Gemma 4 E4B
- [x] Benchmark Qwen3-14B Q4_K_M
- [x] Benchmark Qwen3.8-27B Q4
- [ ] Benchmark Qwen3.5-9B
- [ ] Select primary daily model

### v0.2 — Local API
- [ ] Enable LM Studio local API
- [ ] Test OpenAI-compatible endpoint
- [ ] Add simple API health-check script
- [ ] Test model calls from Python

### v0.3 — Unified UI
- [ ] Install Open WebUI
- [ ] Connect Open WebUI to LM Studio
- [ ] Create General / Coding / Project assistants

### v0.4 — Tools
- [ ] Add trusted filesystem MCP
- [ ] Add Git tooling
- [ ] Add shell/Python tools with restricted permissions
- [ ] Test against a real local project

### v0.5 — Knowledge / RAG
- [ ] Select embedding model
- [ ] Decide vector store
- [ ] Add project documentation knowledge base
- [ ] Benchmark retrieval quality

### v0.6 — Second AI node
- [ ] Record desktop hardware
- [ ] Benchmark desktop GPU
- [ ] Assign node role
- [ ] Connect both machines over LAN
- [ ] Test independent parallel workloads

### v0.7 — Automation
- [ ] Evaluate n8n
- [ ] Add local LLM workflows
- [ ] Add recurring project-support automations

### v0.8 — Agents
- [ ] Start with one agent + tools
- [ ] Add planning loop only where useful
- [ ] Evaluate multi-agent workflows only after single-agent baseline

## Design principles

1. **Useful before impressive.**
2. Prefer one good agent with reliable tools over many agents talking to each other.
3. Keep sensitive/private project data local when possible.
4. Benchmark on actual hardware instead of relying only on leaderboards.
5. Optimize for answer quality at acceptable speed, not tokens/sec alone.
6. Do not give tools unrestricted filesystem or shell access by default.
7. Keep configuration reproducible and version-controlled.
8. Do not commit model weights, caches, secrets or generated vector databases to GitHub.

## Repository layout

```text
local-ai-workstation/
├── README.md
├── PROJECT.md
├── .gitignore
├── configs/
├── scripts/
├── benchmarks/
├── docs/
├── knowledge/
└── notes/
```

## GitHub mirror

Create a new empty GitHub repository, for example:

`local-ai-workstation`

Then from this folder:

```powershell
git init
git add .
git commit -m "Initialize local AI workstation"
git branch -M main
git remote add origin https://github.com/<USERNAME>/local-ai-workstation.git
git push -u origin main
```

After that the normal workflow is:

```powershell
git add .
git commit -m "Describe change"
git push
```

Do not commit API keys, tokens, `.env` files, model files or caches.
