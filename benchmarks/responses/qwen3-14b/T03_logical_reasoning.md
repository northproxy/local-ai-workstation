# Qwen3-14B — T03 Logical Reasoning

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
VRAM used: [record during generation]
System RAM used: [record during generation]
```

## Performance

```text
Tokens/sec:
Time to first token:
Total response time:
Output tokens:
Stop reason:
```

## Prompt

```text
There are four servers: A, B, C, and D.

We know the following:

1. If server A is running, server B is also running.
2. If server B is not running, server C is running.
3. Server C is not running.
4. Server D is running only if server A is running.
5. Server D is running.

Determine the state of each server: running or not running.

Show the conclusion for each server separately and explain which condition it follows from.

If any conditions contradict each other, explicitly point this out.
```

### Expected logical result

```text
A = works
B = works
C = does not work
D = works
```

No contradiction.

## Response

[Paste model response verbatim here.]

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
