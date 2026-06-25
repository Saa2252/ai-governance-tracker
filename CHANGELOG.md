# Changelog

All notable changes — **including score changes** — are recorded here so outside
researchers can audit the index's own decisions over time. This is the index
holding itself to the same evidence-and-versioning standard it asks of every
country. Format follows [Keep a Changelog]; `data/countries.json` → `metadata.version`
is the source of truth.

## [3.x] — 2026-06 (current)
### Added
- **Governance Maturity** score (0–100; staged 0–3 per mechanism) as the primary, discriminating measure.
- 8 high-income **comparators** (overlay), with a default-on 24-country global view.
- **Rankings** leaderboard + CSV export; in-app score-calculation explainer.
- **Robustness analysis** (`analysis/robustness.py`): mechanism correlations (0.10–0.79, no redundancy) and weighting sensitivity (**Spearman ρ = 0.99** vs equal weights).
- Standards **cross-walk** (UNESCO RAM / OECD); `CONTRIBUTING.md`; **update policy** + **watchlist**; this changelog.
### Changed
- Dashboard leads with Maturity; enforcement reframed as a binary "in force" chip + count (no more empty 0/100).

## [3.0] — 2026-06 — all countries evidence-coded
### Changed
- **All 16 Global South countries evidence-coded** — no provisional scores remain.
- Notable score corrections after strict "in-force" coding:
  - **Brazil** implementation 55 → **20** (PL 2338 not enacted; only the ANPD sandbox is in force).
  - **India** 40 → **0**, **Kenya** 25 → **0** (active strategies/guidelines, nothing in force).
  - **Mexico** 40 → **0** (Federal AI Law pending in the Senate).

## [2.1–2.2] — 2026-06
### Changed
- UNESCO & OECD scores made **fact-derived** (RAM status; adherence/membership), each with evidence.
- India OECD relabelled `non_member` (not a formal AI-Principles adherent).
- Confirmed UNESCO RAM completion: Mexico, Kenya (→ UNESCO 45 → 70); Brazil in-progress (→ 55).

## [2.0] — 2026-06 — deterministic index
### Added
- **Deterministic** implementation score (weighted sum of six in-force indicators; machine-verifiable).
- Per-indicator **evidence + citations**; `coding_status` (`evidence_coded` / `provisional`).

## [1.0–1.4] — 2026-05/06
### Added
- Initial release (8 → 16 countries); sourced World Bank figures; OECD/GPAI verified;
  24-country roster + selection logic; per-score `source` citations; scoring rubric.

---

### Logging a change going forward
Any score change must: (1) update the indicator `evidence` + `as_of` + `source`;
(2) add a line here under a new version with the **old → new** value and the reason;
(3) bump `metadata.version`. See [`docs/UPDATE_POLICY.md`](docs/UPDATE_POLICY.md).

[Keep a Changelog]: https://keepachangelog.com/
