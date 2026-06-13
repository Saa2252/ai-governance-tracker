# Contributing

Thanks for helping improve the Global South AI Governance Tracker. The index is
designed to be **contestable and reproducible** — contributions that add evidence,
correct a score, or extend coverage are very welcome.

## Ways to contribute

1. **Evidence-code a country** (turn a `provisional` entry into `evidence_coded`, or
   add a new one) — follow [`coding_worksheet.md`](coding_worksheet.md).
2. **Correct a score** — open an issue or PR citing a *specific, in-force* legal or
   regulatory instrument (with article/section). See "How to contest a score" in
   [`../METHODOLOGY.md`](../METHODOLOGY.md).
3. **Confirm a UNESCO RAM status** currently marked `not_confirmed`, with a link to
   the UNESCO Global AI Ethics & Governance Observatory.
4. **Improve the dashboard, docs, or pipeline.**

## Rules that keep the index credible

- **Every indicator needs a citation.** Each `implementation_status.evidence` entry
  must have a `source` URL and an `as_of` date. No source, no change.
- **Strict "in force" threshold.** Mark a mechanism `true` only if it is *operational
  and in force* — not drafted, proposed, or voluntary. Maturity stages (0–3) capture
  the in-between.
- **Stay mapped to the standards.** New mechanisms should map to a UNESCO RAM
  dimension and an OECD AI Principle (see METHODOLOGY).
- **Validate before you commit.** Run `python analysis/findings.py` (it asserts the
  implementation score equals the weighted sum) and check `data/*.json` is valid JSON.

## Toward multi-coder reliability

Scores are currently single-coder (one analyst). To raise reliability we welcome
**independent re-coding**: open a PR that re-scores a country with your own evidence.
Where two coders diverge, we record both rationales in the PR and reconcile against
the rubric. The goal is a published inter-coder-reliability figure once enough
countries have a second coder.

## Workflow

1. Fork → create a branch (`data/evidence-code-egypt`, `fix/brazil-enforcement`, …).
2. Make the change; keep commits small and use conventional prefixes (`data:`, `docs:`, `fix:`).
3. Open a pull request describing the evidence and citing sources.

By contributing you agree your contributions are licensed under the repository's
MIT License.
