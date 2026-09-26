# Qwen3.5-9B — T01 Explanation / Teaching

## Runtime

```text
Model: Qwen3.5-9B
Exact model/repository: qwen/qwen3.5-9b
Quantization: Q4_K_M
Runtime: LM Studio
Context length: 8192
GPU offload: 32 layers
Reasoning mode: Enabled, budget unrestricted
Temperature: 1
VRAM used: ~6.6 GB during generation
System RAM used: ~5.5 GB (llama-server working set)
```

## Performance

```text
Tokens/sec: 44,29
Time to first token: 0,30 s
Total response time: 42,88 s
Output tokens: 2677
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

System RAM and VRAM differ fundamentally in architecture, access speed, and purpose. System RAM (DDR4/DDR5) is volatile memory managed by the CPU to handle general computing tasks. It offers aggregate bandwidths typically between 100-200 GB/s for dual-channel or quad-channel setups. VRAM (GDDR6/HBM2e) is local memory soldered directly to the GPU die. It offers significantly higher internal bandwidth, often exceeding 500-800 GB/s on modern NVIDIA GPUs like the RTX 40-series.

**Concrete Example:** You have a computer with **32 GB System RAM** and an NVIDIA GPU with **8 GB VRAM**.

**1. Where Model Weights Are Stored**
LLM weights are mathematical matrices required for inference. Ideally, these reside in GPU memory to allow parallel matrix multiplications. Software frameworks (e.g., llama.cpp) attempt to load the entire model into VRAM first. If the quantized model size exceeds 8 GB, it is partitioned: a portion of the weights resides on the 8 GB VRAM (active memory), while the remainder spills over into the 32 GB system RAM via the PCIe bus.

**2. Model Fits Entirely in VRAM**
Consider a quantized 7B parameter model requiring ~5 GB after 4-bit quantization. This fits comfortably within 8 GB VRAM. All weight matrices reside on the GPU die. During inference, the GPU cores fetch weights directly from high-speed local memory. No data transfer occurs across the PCIe bus. The latency is minimal, and throughput reaches its peak potential (tokens per second), as the GPU spends almost all cycles performing computation rather than waiting for data movement.

**3. Model Does Not Fit in VRAM**
If you attempt to run a 14B parameter model (~8.5 GB quantized), it exceeds the 8 GB limit. The system must offload parts of the weight matrix to system RAM. During the inference step, only a subset of layers is active on the GPU while others wait in CPU memory.

**4. Why Performance Drops Sharply**
The performance drop stems from the PCIe bus bottleneck. To load weights from 32 GB system RAM into VRAM for calculation, data must cross the PCIe Gen 4 x16 interface, offering approximately 32 GB/s aggregate bandwidth. This is roughly ten times slower than internal VRAM bandwidth. When weights reside in system RAM, the GPU halts computation while waiting for data transfer packets to arrive across the PCIe bridge. This idle time drastically reduces tokens-per-second compared to a model fitting entirely in VRAM, where no such wait occurs.

**5. Role of KV Cache**
The Key-Value (KV) cache stores intermediate states from previous tokens during generation to enable attention mechanisms. If weights are offloaded due to VRAM constraints, the available space for the KV cache shrinks significantly. As the model generates text, the KV cache grows linearly with context length. With only 3 GB of free space remaining in VRAM (after loading an 8 GB weight set), a growing KV cache will rapidly fill the remaining buffer. This forces additional swapping of active layers between VRAM and system RAM to accommodate new cache entries. Consequently, the GPU cannot sustain high-speed generation because it constantly swaps both weights and cache data over the PCIe bus, further compounding latency.

**Summary**
In local LLMs, VRAM determines the maximum model size that can run at full speed. System RAM acts as a secondary storage buffer accessed via slower PCIe links. When VRAM capacity is exceeded by model size or KV cache growth, the system relies on the slower PCIe bus to fetch data, creating a bandwidth bottleneck that reduces inference speed regardless of the amount of total system memory available.

## Quality scoring

| Metric | Score /10 | Notes |
|---|---:|---|
| Correctness | 6 | Several technical oversimplifications/inaccuracies: VRAM is not generally 'soldered directly to the GPU die'; partial offload does not necessarily mean weights are swapped over PCIe for every token; KV-cache behavior is described too simplistically; the '3 GB free after loading an 8 GB weight set' example is internally inconsistent. |
| Reasoning | 7 | The explanation follows a useful causal chain (capacity → placement → bandwidth → latency), but some conclusions rely on an oversimplified offload model. |
| Instruction following | 10 | Covers all five requested points, uses the specified 32 GB RAM / 8 GB VRAM example, avoids analogies, and stays within 700 words. |
| Clarity | 9 | Well structured and easy to follow despite the technical inaccuracies. |
| Conciseness | 8 | Mostly focused, with some repeated explanation of PCIe/offload effects. |
| Practical usefulness | 7 | Useful for building intuition, but the inaccurate offload/KV-cache details could lead to wrong expectations when tuning local inference. |
| Subjective quality | 7 | Strong presentation, but technical precision is not yet good enough for a daily reference answer. |

## Comparison notes

```text
Strengths:

Weaknesses:

Hallucinations / factual errors:

Instruction violations:

Better than Qwen3-14B:

Worse than Qwen3-14B:

Would I use this answer every day? YES / NO
```
