# Benchmark Responses

Store every raw model response as a separate Markdown file.

Recommended structure:

```text
benchmarks/
├── MODEL_TEST_PROMPTS_EN.md
├── BENCHMARK_RESULTS.md
└── responses/
    ├── qwen3.5-9b/
    │   ├── T01_explanation.md
    │   ├── T02_troubleshooting.md
    │   ├── T03_logical_reasoning.md
    │   ├── T04_coding.md
    │   └── T05_instruction_following.md
    ├── qwen3-14b-q4_k_m/
    │   └── ...
    └── gemma-4-e4b/
        └── ...
```

## Rules

1. Use one file per model per test.
2. Keep the exact benchmark prompt.
3. Copy the model response verbatim.
4. Do not fix grammar, code, formatting, or factual errors.
5. Record runtime metrics immediately after generation.
6. Use the same filename pattern for every model.
7. Commit raw benchmark responses to Git so comparisons remain reproducible.

## Filename convention

```text
T01_explanation.md
T02_troubleshooting.md
T03_logical_reasoning.md
T04_coding.md
T05_instruction_following.md
T06_linux_analysis.md
T07_architecture.md
T08_summarization.md
T09_ambiguity.md
T10_planning.md
TR1_reasoning_ab.md
TL1_long_response_control.md
```

For a reasoning A/B test, either keep both runs in one file clearly marked `Reasoning OFF` / `Reasoning ON`, or use:

```text
TR1_reasoning_off.md
TR1_reasoning_on.md
```

The second approach is better for Git diff.
