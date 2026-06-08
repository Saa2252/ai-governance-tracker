# Scoring Rubric & Worked Examples

This document makes the scores **auditable**. It states the rubric, then shows —
for a high, a mid, and a low case — exactly how documented evidence maps to a
number. Every score in `data/countries.json` carries a `source` (primary
instrument + framework reference) so any reader can trace it back.

> **Honesty note.** Framework-alignment and implementation scores are *expert
> assessments*, not measured quantities. The rubric below is what makes them
> consistent and contestable. Factual fields (internet access, data-protection
> laws, OECD/GPAI membership) are separately sourced and verifiable.

---

## A. Framework Adoption Score (0–100)

How closely a country's **written policy/law** aligns with a given framework.

| Band | Label | What must be true (evidence threshold) |
|------|-------|-----------------------------------------|
| 80–100 | High | A binding instrument (enacted or advanced bill) that directly mirrors the framework's structure (e.g. EU risk tiers) across most provisions. |
| 50–79 | Partial | A strategy or bill that selectively adopts core concepts (risk-based approach, transparency) but modifies or omits significant parts. |
| 20–49 | Low | The framework is referenced or endorsed rhetorically; little structural correspondence. |
| 0–19 | None | No meaningful reference or alignment. |

## B. Implementation Score (0–100)

How much governance is **actually operational**. Six weighted components; a
country earns the weight only when the mechanism is *in force*, not merely planned.

| Component | Weight | Earns the points when… |
|-----------|-------:|------------------------|
| Enforcement body | 25 | A designated authority with an explicit AI mandate is operating. |
| Regulatory sandbox | 20 | An AI testing sandbox is live and accepting participants. |
| Impact assessments | 20 | AI impact assessments are *mandatory* for defined uses. |
| Transparency requirements | 15 | Disclosure obligations are in force. |
| Audit mechanisms | 10 | Third-party audit provisions exist. |
| Redress mechanisms | 10 | Channels for affected people to seek remedy exist. |

The `overall_score` is the sum of earned weights (then sanity-checked against the
country's stage). The booleans that drive it are stored in
`implementation_status` for full transparency.

---

## C. Worked examples

### 1. HIGH — Brazil, EU AI Act adoption = **75** (`partial`→ high end)

**Evidence.** AI Bill **PL 2338/2023** establishes a risk-based regime that
mirrors the EU AI Act's tiers (unacceptable/high/limited), mandates algorithmic
impact assessments, and creates a national authority. It adds an environmental-
impact consideration not in the EU text.
*Source: PL 2338/2023; EBIA strategy (2021).*

**Mapping.** Direct structural correspondence on risk tiers and impact
assessments → top of the "Partial" band rather than "High (80+)" because the bill
was not yet fully enacted/operational at time of scoring. → **75**.

**Implementation = 55:** enforcement body (25) + sandbox (20) + impact
assessments (20) + transparency (15) are in force = 80 of available weight, but
audit (0) and redress (0) absent, and several provisions still phasing in →
scored **55** overall.

**Gap = 75 − 55 = 20** (widest single-country gap in the dataset): strong law,
enforcement machinery still maturing.

### 2. MID — India, EU AI Act adoption = **45** (`partial`)

**Evidence.** The **Digital India Act (draft, 2023)** incorporates a risk-based
approach, but its high-risk categories diverge from Annex III (e.g. agricultural
AI treated as critical infrastructure). No binding horizontal AI law yet.
*Source: Digital India Act draft; NITI Aayog National Strategy for AI (2018).*

**Mapping.** Core risk-based concept present but structurally divergent and
non-binding → middle of "Partial" → **45**.

**Implementation = 40:** sandbox (20) + impact assessments (20) in force;
**no** enforcement body (0), transparency (0), audit (0), redress (0) → **40**.

### 3. LOW — Nigeria, EU AI Act adoption = **25** (`low`)

**Evidence.** The **National AI Strategy (NITDA, 2024)** focuses on adoption and
local priorities (fintech, agriculture, oil & gas, electoral integrity) and
references EU ideas only loosely; no risk-tier statute.
*Source: NITDA National AI Strategy (2024); draft governance framework.*

**Mapping.** Framework referenced, minimal structural correspondence → "Low" →
**25**.

**Implementation = 20:** none of the six mechanisms operational at time of
scoring → low score reflecting an early-stage governance environment.

---

## D. Reproducibility

- Each score's `source` field names the instrument it rests on.
- The headline statistics in the README are computed from this data in
  [`analysis/`](../analysis/).
- Disagree with a score? Open an issue citing the instrument and the band above —
  the rubric is meant to be argued with.

*Last updated: 2026-06-04*
