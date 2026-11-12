# CB01 — GitHub documentation update (2026-11-12)

Copy the contents of this ZIP into the root of the `northproxy/local-ai-workstation` checkout, retaining the relative paths:

- `PROJECT.md` — **updated version** of the supplied project document; replace the existing root file only after reviewing the diff.
- `benchmarks/coding_benchmark_v1/MODEL_CONFIGURATIONS.md` — identities, original LM Studio screenshots, initial vs intended settings, unknown values.
- `benchmarks/coding_benchmark_v1/BENCHMARK_PROTOCOL.md` — measurement, fairness, scoring, official run / diagnostic distinction, API gate.
- `benchmarks/coding_benchmark_v1/KNOWN_ISSUES.md` — observed failures, separate hypotheses, missing telemetry, follow-ups.

Existing prompt/rubric/evaluator/results/Run01 files are **not modified** by this update. Commit these four files only after reviewing the source-control diff. No GitHub changes were made automatically.

Suggested commit title:
`docs(benchmark): record CB01 configurations and runtime findings`
