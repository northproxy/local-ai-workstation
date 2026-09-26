# LM Studio Settings — Qwen3-14B

Короткая конфигурация для Core Benchmark T01–T05.

## Model / load

```text
Model: Qwen3-14B
Exact model/repository: lmstudio-community/Qwen3-14B-GGUF
Model file: Qwen3-14B-Q4_K_M.gguf
Format: GGUF
Quantization: Q4_K_M
Architecture: qwen3
Size on disk: 9.00 GB

Context length: 8192
Model maximum context: 32768
GPU offload: 40 layers

CPU thread pool size: 12
Evaluation batch size: 2048
Physical batch size: 512
Max concurrent predictions: 4

Unified KV Cache: Enabled
Offload KV Cache to GPU Memory: Enabled
Keep Model in Memory: Enabled
Try mmap(): Enabled
Speculative Decoding: Off
Flash Attention: Enabled
```

## Inference / reasoning

Для прямого сравнения с Qwen3.5-9B использовать те же параметры:

```text
Enable Thinking: Enabled
Reasoning budget: Unrestricted

Temperature: 1
Top K: 20
Top P: 0.95
Presence penalty: 1.5
Repeat penalty: Disabled
Min P: Disabled
Seed: Random
```

## Changes from current Qwen3-14B defaults

Перед Core Benchmark изменить:

```text
Temperature: 0.8 -> 1
Top K: 40 -> 20
Repeat penalty: 1.1 -> Disabled
Presence penalty: Disabled -> 1.5
Min P: 0.05 -> Disabled
```

Оставить без изменений:

```text
Enable Thinking: Enabled
Reasoning budget: Unrestricted
Top P: 0.95
```

## Record during generation

```text
VRAM used:
System RAM used:
```

VRAM:

```powershell
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv -l 1
```

RAM: зафиксировать working set процесса `llama-server`.

## Benchmark note

Эти sampling-параметры выбраны не как рекомендуемые настройки Qwen3-14B, а для максимально чистого сравнения с уже выполненным Qwen3.5-9B Core Benchmark.

После выбора модели можно отдельно подобрать оптимальные daily-use settings для победителя.
