# Local LLM Benchmark Results

This file stores comparable benchmark results for local LLMs.

Use the exact prompts from `MODEL_TEST_PROMPTS_EN.md`.

---

# Summary

| Model | Quant | Test | Tok/s | TTFT | Output tokens | Quality score | Notes |
|---|---|---|---:|---:|---:|---:|---|
| Qwen3.5-9B | Q4_K_M | TEST 1 — Explanation / Teaching | 44.29 | 0.30 s | 2677 | 7.7 | Daily-use verdict: pending |
| Qwen3.5-9B | Q4_K_M | TEST 2 — Troubleshooting | 44.71 | 0.40 s | 3118 | 6.3 | Daily-use verdict: pending |
| Qwen3.5-9B | Q4_K_M | TEST 3 — Logical Reasoning | 44.28 | 0.53 s | 3520 | 9.1 | Daily-use verdict: pending |
| Qwen3.5-9B | Q4_K_M | TEST 4 — Coding / Debugging | 43.46 | 0.48 s | 3283 | 9.1 | Daily-use verdict: pending |
| Qwen3.5-9B | Q4_K_M | TEST 5 — Instruction Following | 43.68 | 0.46 s | 3004 | 8.4 | Daily-use verdict: pending |

| Qwen3-14B | Q4_K_M | T01 — Explanation / Teaching | 1.60 | 106.95 s | 1395 | 7.2* | 40 layers; old run, runtime not directly comparable |
| Qwen3-14B | Q4_K_M | T02 — Troubleshooting | 13.29 | 1.74 s | 1050 | 7.2* | 32 layers; Thinking 33.81 s; total time not recorded |
| Qwen3-14B | Q4_K_M | T03 — Logical Reasoning | 12.25 | N/R | 1437 | 9.5* | 32 layers; runtime total 122.32 s |
| Qwen3-14B | Q4_K_M | T04 — Coding / Debugging | 11.25 | N/R | 1463 | 9.2* | Offload 40 in supplied file; verify; runtime total 135.26 s |
| Qwen3-14B | Q4_K_M | T05 — Instruction Following | 14.75 | 0.79 s | 552 | 9.8* | 32 layers; UI values; supplied log mismatch |

### Core benchmark snapshot

```text
Mean quality score across T01–T05: 8.1/10
Daily-use verdict: pending user evaluation
```

The current result suggests that Qwen3.5-9B is a strong interactive-speed candidate, with especially strong results on logical reasoning and coding. The weakest Core result is Windows/DNS troubleshooting, where several diagnostic recommendations were technically questionable. Daily-use preference is intentionally left unresolved until the user has enough real-world experience with the model.

---

## Qwen3-14B — Core benchmark completion (2026-11-12)

T01–T05 responses have been captured. Assistant technical scores use **six** metrics (Correctness, Reasoning, Instruction following, Clarity, Conciseness, Practical usefulness) and exclude the user's **Subjective quality**, which remains pending.

| Test | Qwen3-14B six-metric mean | Qwen3.5-9B six-metric mean (recalculated from existing rubric) |
|---|---:|---:|
| T01 | 7.17 | 7.83 |
| T02 | 7.17 | 6.50 |
| T03 | 9.50 | 9.17 |
| T04 | 9.17 | 9.17 |
| T05 | 9.83 | 8.50 |
| **Core mean** | **8.57** | **8.23** |

*Scores in the summary table marked with `*` are rounded six-metric assistant scores, not the earlier seven-metric published Qwen3.5-9B scores. The pre-existing 8.1/10 Qwen3.5-9B snapshot includes an assistant-assigned subjective metric; it is intentionally preserved as historical data, not directly compared to 8.57.*

**Comparability limitations:** Qwen3-14B T01 ran at 40 GPU layers and 1.60 tok/s, while later tests were intended to run at 32 layers; the submitted T04 file still records 40 layers, so the actual setting needs verification. Sampling temperature on the 14B submissions is not confirmed. T05 GUI reported 552 tokens / 14.75 tok/s / 18.90 s Thinking, but the submitted runtime log for that interval reported just 10 generated tokens; the two must not be conflated. Some output-token metrics include thinking tokens; final-answer length and total latency are distinct.

**Provisional daily-model recommendation:** Qwen3.5-9B as the faster interactive default, Qwen3-14B as an optional quality-check model when latency is acceptable. Final selection awaits user subjective evaluation and matching run settings.

---

# Model: Qwen3.5-9B

## Runtime configuration

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

---

## TEST 1 — Explanation / Teaching

### Performance

```text
Tokens/sec: 44,29
Time to first token: 0,30 s
Total response time: 42,88 s
Output tokens: 2677
Stop reason: EOS Token Found
```

### Quality scoring

| Metric | Score | Notes |
|---|---:|---|
| Correctness | 6 | Several technical oversimplifications/inaccuracies: VRAM is not generally 'soldered directly to the GPU die'; partial offload does not necessarily mean weights are swapped over PCIe for every token; KV-cache behavior is described too simplistically; the '3 GB free after loading an 8 GB weight set' example is internally inconsistent. |
| Reasoning | 7 | The explanation follows a useful causal chain (capacity → placement → bandwidth → latency), but some conclusions rely on an oversimplified offload model. |
| Instruction following | 10 | Covers all five requested points, uses the specified 32 GB RAM / 8 GB VRAM example, avoids analogies, and stays within 700 words. |
| Clarity | 9 | Well structured and easy to follow despite the technical inaccuracies. |
| Conciseness | 8 | Mostly focused, with some repeated explanation of PCIe/offload effects. |
| Practical usefulness | 7 | Useful for building intuition, but the inaccurate offload/KV-cache details could lead to wrong expectations when tuning local inference. |
| Subjective quality | 7 | Strong presentation, but technical precision is not yet good enough for a daily reference answer. |

### Overall score

```text
Average quality score: 7.7/10
Would I use this answer every day? Pending user evaluation
```

## TEST 2 — Troubleshooting

### Performance

```text
Tokens/sec: 44,71
Time to first token: 0,40 s
Total response time: 52,22 s
Output tokens: 3118
Stop reason: EOS Token Found
```

### Quality scoring

| Metric | Score | Notes |
|---|---:|---|
| Correctness | 5 | Contains several important diagnostic errors: private/router DNS is treated as suspicious; NXDOMAIN from nslookup is misinterpreted as inability to reach the DNS server; the IPv6 step is inappropriate; stale DNS cache is ranked too highly as a general cause. |
| Reasoning | 5 | The overall DNS-focused diagnosis is correct, but the troubleshooting order changes state before gathering enough evidence and some result interpretations do not logically follow. |
| Instruction following | 8 | Provides commands, explanations and result interpretation, avoids reinstalling drivers/Windows, and does not invent outputs; however, the early stack/IPv6 changes are more invasive than the requested safest-first approach suggests. |
| Clarity | 8 | Readable step-by-step structure with explicit commands and interpretations. |
| Conciseness | 8 | Reasonably focused; little unnecessary material. |
| Practical usefulness | 5 | Parts are usable, but an administrator should correct the nslookup interpretation and avoid the proposed IPv6 change before following this plan. |
| Subjective quality | 5 | Looks confident and organized, but contains enough operationally risky/misleading advice that I would not use it unedited. |

### Overall score

```text
Average quality score: 6.3/10
Would I use this answer every day? Pending user evaluation
```

## TEST 3 — Logical Reasoning

### Performance

```text
Tokens/sec: 44,28
Time to first token: 0,53 s
Total response time: 64 s
Output tokens: 3520
Stop reason: EOS Token Found
```

### Quality scoring

| Metric | Score | Notes |
|---|---:|---|
| Correctness | 10 | Matches the expected result exactly: A running, B running, C not running, D running; no contradiction. |
| Reasoning | 10 | Correctly uses contraposition for condition 2 and interprets 'D only if A' as D → A. |
| Instruction following | 10 | Gives a separate conclusion and derivation for each server and explicitly checks for contradictions. |
| Clarity | 9 | Very clear, with explicit symbolic logic and a final consistency check. |
| Conciseness | 7 | More verbose than necessary for a small logic problem; the summary and consistency discussion repeat earlier conclusions. |
| Practical usefulness | 9 | Directly usable and easy to verify. |
| Subjective quality | 9 | Strong reasoning answer; only slightly over-explained. |

### Overall score

```text
Average quality score: 9.1/10
Would I use this answer every day? Pending user evaluation
```

## TEST 4 — Coding / Debugging

### Performance

```text
Tokens/sec: 43,46
Time to first token: 0,48 s
Total response time: 60 s
Output tokens: 3283
Stop reason: EOS Token Found
```

### Quality scoring

| Metric | Score | Notes |
|---|---:|---|
| Correctness | 9 | Finds the real bug, gives the expected output, and uses the appropriate normalized set. One statement is slightly too absolute: user.lower() can match result when the first stored spelling is already lowercase. |
| Reasoning | 9 | Correctly explains the mismatch between normalized comparisons and original-cased storage, and connects the set solution to average O(1) membership checks. |
| Instruction following | 10 | Addresses all seven requested items, preserves order/casing, uses no third-party libraries, and does not unnecessarily redesign the task. |
| Clarity | 9 | Clear explanation and readable corrected code. |
| Conciseness | 8 | Some repetition from mirroring every numbered requirement, but still controlled. |
| Practical usefulness | 10 | The corrected function is directly usable and matches the expected behavior. |
| Subjective quality | 9 | A strong coding/debugging answer suitable for daily use. |

### Overall score

```text
Average quality score: 9.1/10
Would I use this answer every day? Pending user evaluation
```

## TEST 5 — Instruction Following

### Performance

```text
Tokens/sec: 43,68
Time to first token: 0,46 s
Total response time: 62 s
Output tokens: 3004
Stop reason: EOS Token Found
```

### Quality scoring

| Metric | Score | Notes |
|---|---:|---|
| Correctness | 7 | Core CIDR values are correct, but the broadcast address is incorrectly called the 'highest usable number'; it is not a usable host address. 'Every device connected to the network' is also broader than the relevant subnet/broadcast domain. |
| Reasoning | 8 | The prefix-length-to-mask/network/broadcast explanation is coherent, though this task requires little explicit reasoning. |
| Instruction following | 10 | Exactly 5 bullet points, no headings/table/conclusion, no bullet exceeds 2 sentences, and every required CIDR detail is included. |
| Clarity | 9 | Clear and accessible wording. |
| Conciseness | 9 | Compact and disciplined while satisfying all constraints. |
| Practical usefulness | 8 | Useful as a quick explanation after correcting the broadcast-address wording. |
| Subjective quality | 8 | Excellent formatting discipline; minor networking inaccuracies keep it below top-tier. |

### Overall score

```text
Average quality score: 8.4/10
Would I use this answer every day? Pending user evaluation
```


# How to score consistently

## Correctness
- 10 = fully correct
- 8 = minor issue, no practical impact
- 5 = important omission or partial error
- 0 = fundamentally wrong

## Reasoning
- 10 = clear, logically valid, well-prioritized
- 8 = good reasoning with minor gaps
- 5 = mostly plausible but shallow or inconsistent
- 0 = invalid reasoning

## Instruction following
- 10 = all explicit requirements followed
- 8 = one minor violation
- 5 = several requirements missed
- 0 = largely ignored prompt constraints

## Clarity
- 10 = very easy to follow
- 8 = clear with minor roughness
- 5 = understandable but confusing in places
- 0 = difficult to understand

## Conciseness
- 10 = no unnecessary content
- 8 = slightly verbose
- 5 = substantially overlong
- 0 = highly bloated or repetitive

## Practical usefulness
- 10 = directly usable
- 8 = useful with small edits
- 5 = needs substantial correction
- 0 = not useful

## Subjective quality
Personal preference. Do not try to make this objective.

---

# Recommended benchmark workflow

For every model:

1. Use a fresh chat.
2. Use the exact same prompt.
3. Keep temperature and context settings identical when possible.
4. Record runtime metrics immediately.
5. Score the answer before looking at another model's answer if possible.
6. Add one or two short notes about what stood out.
7. After all models complete the same test, compare them side-by-side.
8. Update the Summary table.

The most important fields are:

```text
Tok/s
TTFT
Correctness
Instruction following
Practical usefulness
Subjective quality
```

These are enough to make a useful decision without turning the benchmark into a full research project.
