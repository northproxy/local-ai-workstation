# CB01 — Known Issues and Diagnostics

**Last updated:** 2026-11-12  
**Status convention:** `Observed` = directly supported by user logs/screenshots; `Hypothesis` = plausible, not proven; `Open` = not diagnosed/resolved.

## ISS-01 — Repetitive generation and incomplete code (Observed, Open)

**Affected run:** `CB01-Qwen3.5-9B-Run01`, 2026-11-12. The archived answer contained many repeated `Wait:`-style requirement restatements (previous review counted 808 occurrences), produced **no complete `integrity.py` or `test_integrity.py`**, and reached the context boundary. This fails the deliverable requirement; no automated suite was executed against model code.

**What we know:** Runtime log reported 15589 generated tokens at 44.02 tok/s, generation time 354081.92 ms, overall processing time 354663.60 ms, and `truncated = 1`. A separate subsequent short request appeared in the log, but its role is not confirmed.

**What we do not know:** Whether the primary trigger was model behavior, thinking/template handling, stop conditions, a Chat UI/runtime limit interaction, or a combination. The `Thinking Process:` text in the raw output is **not proof** that the LM Studio UI switch was On.

**Next diagnostic:** Controlled short request to inspect effective thinking/template behavior, plus bounded token generation over a verified API endpoint. Repeat with the unchanged CB01 prompt only after freezing a workable protocol; assign a distinct Run ID.

## ISS-02 — LM Studio Chat response-length input rejects >2048 (Observed, Open)

The user attempted `Limit Response Length = 8192` and reported that the red validation border remained; values **above 2048 were not accepted** in their installation. This is an observed UI behavior, **not proof of an engine-wide or API-wide 2048-token limit**. Specific LM Studio app/engine versions are not recorded; do not attribute a precise upstream bug without that evidence.

**Consequence:** The agreed 8192-token cap was not verified to have taken effect for Run01. No fair comparison may claim an 8192-token cap was enforced.

**Next diagnostic:** Record LM Studio version, test the relevant API route using its documented parameter name and verify stop reason and output tokens. An API route may not share the UI validator; this requires local confirmation. Do not reduce benchmark prompt/output requirements for only one model.

## ISS-03 — Context overflow / truncation at 16384 (Observed, Open)

**Evidence:** Run01 log `n_gen = 15589`, 795 prompt-eval tokens, `total time ... / 16384 tokens` and slot release `n_tokens = 16383, truncated = 1`. A post-run screenshot displayed `Context Overflow = Truncate Middle`; this does **not** independently prove which overflow policy was effective during the submitted request.

**Risk:** Large repetitive output can fill the context before the intended program is delivered. Truncation can distort the first-pass evaluation. Set/verify a bounded output policy, consider `Stop at Limit` to prevent silent context rewriting, record the actual stop conditions.

## ISS-04 — Configuration/telemetry gaps (Observed, Open)

Unrecorded: LM Studio app/engine build; GPU/CPU peak memory; prompt-to-first-token latency; backend version; precise user-request-to-first-token wall time; actual effective sampling/seed/penalties/offload at the moment of Run01. Qwen3.8-27B repository ID was truncated in its screenshot and is provisional.

**Action:** Fill the run metadata table from measured session data. Preserve `TBD`/`not measured` rather than estimating these values, and keep pre-tuning inventory distinct from effective runtime configuration.

## What not to conclude yet

- Do not infer that all Qwen3.5-9B coding attempts fail from one run.
- Do not infer coding quality from 44.02 tok/s.
- Do not assume `Thinking Disabled` guarantees absence of generated reasoning text.
- Do not infer 2048 as a hard limit of LM Studio's API or inference engine from a Chat UI input validator.
- Do not claim 12 automated tests were executed on a non-existent `integrity.py`.

## Follow-up checklist

- [ ] Record exact LM Studio and engine build.
- [ ] Verify API readiness on loopback and actual model endpoint/ID.
- [ ] Verify correct request field for response cap on the selected endpoint.
- [ ] Test enforced output length, stop reason and Thinking disabled using a separate diagnostic prompt.
- [ ] Fix and freeze a comparable CB01 execution protocol for all models.
- [ ] Archive any diagnostic/retry separately as Run02, without replacing Run01.
