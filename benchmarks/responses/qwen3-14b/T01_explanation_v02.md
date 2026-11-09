# Qwen3-14B — T01 Explanation / Teaching

## Runtime

```text
Model: Qwen3-14B
Exact model/repository: lmstudio-community/Qwen3-14B-GGUF
Quantization: Q4_K_M
Runtime: LM Studio
Context length: 8192
GPU offload: 40 layers
Reasoning mode: [verify before benchmark]
Temperature: [verify before benchmark]
VRAM used: ~7.0 GB during generation
System RAM used: ~11.9 GB (llama-server working set)
```

## Performance

```text
Tokens/sec: 1.60
Time to first token: 43.53 s
Total response time: 6 m 42 s
Output tokens: 1312
Stop reason: EOS Token Found
```

## Prompt

```text
Explain the difference between RAM and VRAM so that I understand not only the definitions, but also why this difference is critical when running local LLMs.

Use a concrete example of a computer with:
- 32 GB RAM
- an NVIDIA GPU with 8 GB VRAM

Explain:
1. where the model weights are stored;
2. what happens if the model fits entirely in VRAM;
3. what happens if the model does not fit in VRAM;
4. why performance can drop sharply;
5. what role the KV cache plays.

Do not use analogies such as "a desk and a cabinet." Explain it technically, but clearly.
Maximum 700 words.
```

## Response

RAM (Random Access Memory) is a general-purpose volatile memory managed by the CPU, used for temporary data storage during computation. VRAM (Video RAM) is specialized memory on the GPU, optimized for high-bandwidth parallel processing tasks like matrix multiplication in LLMs. The difference between them is critical when running local LLMs because VRAM enables direct GPU memory access to model weights, while RAM requires slower PCIe transfers.

1. Where the model weights are stored

In a system with 32 GB RAM and an NVIDIA GPU with 8 GB VRAM, model weights are prioritized for storage in VRAM first. Software frameworks attempt to load all or as much of the quantized model as possible into VRAM. If the model size (e.g., 7B parameters quantized to ~5 GB) exceeds VRAM capacity, remaining weights are stored in system RAM via the PCIe bus.

2. What happens if the model fits entirely in VRAM

When the model is fully contained within VRAM (e.g., a 7B parameter model), all weight matrices and intermediate computations occur entirely within the GPU memory. This avoids PCIe data transfers, allowing the GPU to perform parallel matrix multiplications at its peak bandwidth (up to 800 GB/s on modern NVIDIA GPUs). No latency is introduced by memory swapping or external storage.

3. What happens if the model does not fit in VRAM

If the model exceeds VRAM capacity (e.g., a 14B parameter model quantized to ~8.5 GB), the system must offload portions of the weights into system RAM. During inference, the GPU alternates between accessing active layers in VRAM and fetching inactive layers from RAM via PCIe. This introduces frequent data transfers across the PCIe bus (32 GB/s peak bandwidth) instead of leveraging VRAM’s internal high-speed access.

4. Why performance can drop sharply

Performance drops because the PCIe bus introduces latency and bandwidth limitations compared to VRAM. For example, a 14B model would require ~50% of its weights to be swapped between VRAM and RAM during inference. Each data transfer across PCIe adds overhead, reducing the GPU’s ability to sustain high-throughput matrix operations. This leads to significant slowdowns in tokens-per-second compared to models that fit entirely in VRAM.

5. What role the KV cache plays

The Key-Value (KV) cache stores intermediate attention states during generation to enable autoregressive processing. If the model is partially offloaded to system RAM, the available VRAM space for the KV cache shrinks. As context length increases, the KV cache grows linearly, consuming more VRAM. Once the KV cache exceeds available VRAM (e.g., 8 GB total), additional swaps between VRAM and system RAM are required, further degrading performance due to repeated PCIe transfers.

This distinction between RAM and VRAM is critical because VRAM directly enables the high-speed parallelism required for LLM inference, while system RAM introduces bottlenecks through slower interconnects. The 8 GB VRAM in the example limits the maximum model size that can run at full speed without performance degradation, even though 32 GB of system RAM is available.

## Quality scoring

| Metric | Score /10 | Notes |
|---|---:|---|
| Correctness |  | |
| Reasoning |  | |
| Instruction following |  | |
| Clarity |  | |
| Conciseness |  | |
| Practical usefulness |  | |
| Subjective quality |  | |

## Comparison notes

```text
Strengths:

Weaknesses:

Hallucinations / factual errors:

Instruction violations:

Better than Qwen3.5-9B:

Worse than Qwen3.5-9B:

Would I use this answer every day? YES / NO / PENDING
```
