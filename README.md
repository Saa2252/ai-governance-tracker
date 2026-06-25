# 🌍 Global South AI Governance Tracker

**Interactive dashboard mapping AI governance adoption across developing economies**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-governance-tracker.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## The Problem

The EU AI Act takes effect **August 2, 2026**. While frameworks exist at the global level (EU AI Act, UNESCO AI Ethics), there's a critical gap: **how are developing economies actually implementing these frameworks?**

Most AI governance research focuses on the US, EU, and China. But the Global South—representing 85% of the world's population—faces unique challenges:
- Limited regulatory capacity
- Infrastructure constraints  
- Different risk priorities (e.g., agricultural AI vs. autonomous vehicles)
- Dependency on foreign AI systems

This tracker fills that gap with **implementation data from the ground level**.

---

## What This Project Does

📊 **Interactive Dashboard** — Compare AI governance adoption across **16 fully-profiled** developing economies (with a documented [24-country roster](data/country_roster.json) for expansion)

🗺️ **Implementation Mapping** — Track which countries have adopted, adapted, or created alternatives to major frameworks

📈 **Gap Analysis** — Identify where policy exists but implementation lags

🔍 **Risk Category Breakdown** — See how countries classify AI systems differently than EU definitions

---

## Scope & coverage

**This is a transparent _sample_, not a global census.** It covers **16 Global South
countries** (fully evidence-coded) plus **8 high-income comparators**, chosen by
explicit, reproducible criteria — not an arbitrary pick:

- The **in-scope rule** (income + UN region + governance-to-track) and the full
  **24-country roster** (with borderline exclusions and reasons) live in
  [`data/country_roster.json`](data/country_roster.json) and `METHODOLOGY.md`.
- **Expansion path:** the roster marks which in-scope countries are profiled vs.
  pending; coverage grows by evidence-coding the rest via
  [`docs/coding_worksheet.md`](docs/coding_worksheet.md).

It does **not** claim full UN-membership coverage. Read it as a *Global South
governance sample with high-income benchmarks*, expanding by a documented protocol.

---

## Data Sources

This tracker is built on primary research from:

- **UN Development Coordination Office** — Policy implementation data from 7 country offices across 4 regions
- **National AI strategies** — Official government documents (16 countries fully profiled; broader roster screened against the OECD.AI Policy Observatory)
- **Regulatory filings** — Draft and enacted AI legislation
- **Expert interviews** — Practitioners implementing AI governance on the ground

*Methodology details: [METHODOLOGY.md](METHODOLOGY.md)*

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Saa2252/ai-governance-tracker.git
cd ai-governance-tracker

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app/dashboard.py
```

---

## Project Structure

```
ai-governance-tracker/
├── README.md                 # You are here
├── METHODOLOGY.md            # Methodology, scoring, standards cross-walk
├── CITATION.cff              # "Cite this repository" metadata
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── .github/workflows/
│   └── refresh-data.yml      # Scheduled World Bank data refresh (CI)
├── data/
│   ├── countries.json              # 16 Global South profiles (all evidence-coded)
│   ├── comparators_developed.json  # 8 high-income comparators (optional overlay)
│   ├── country_roster.json         # 24-country in-scope roster + selection logic
│   ├── frameworks.json             # EU AI Act / UNESCO / OECD definitions
│   ├── risk_categories.json        # Risk taxonomy vs. the EU baseline
│   └── benchmarks.json             # External indices (Oxford GAIRI, GIRAI)
├── app/
│   └── dashboard.py          # Streamlit interactive dashboard
├── analysis/
│   └── findings.py           # Reproduces every README statistic from the data
├── scripts/
│   └── refresh_world_bank.py # Pulls live World Bank figures (run by the Action)
└── docs/
    ├── data_dictionary.md    # Plain-English definition of every field
    ├── scoring_rubric.md     # Rubric + worked examples
    ├── coding_worksheet.md   # Per-country evidence-coding protocol
    ├── data_pipeline.md      # 3-layer freshness model
    └── CONTRIBUTING.md       # How to contribute / contest a score
```

---

## Key Findings

*All **16 countries are fully evidence-coded** — every implementation indicator
carries a citation, and the Implementation Score is the deterministic weighted sum
of six *in-force* mechanisms (reproduce with [`analysis/findings.py`](analysis/findings.py)).*

| Finding | Evidence (all 16, evidence-coded) |
|---------|-----------------------------------|
| **AI governance is overwhelmingly aspirational** | **Average in-force implementation is just 2/100**, against an average EU AI Act *adoption* of 42/100 — a **~40-point** adoption–enforcement gap. |
| **No operational enforcement anywhere** | **0 of 16** countries have an operational AI enforcement body. Only **2 of 16** have *any* in-force mechanism: **Brazil** (an ANPD regulatory sandbox) and **Vietnam** (mandatory AI content-labelling, in force since 1 March 2026). |
| **Bills, not laws** | Comprehensive AI bills exist (Brazil's PL 2338, Mexico's Federal AI Law, Nigeria's NITDA framework, Thailand's Royal Decree) but remain **pending** — so adoption scores are moderate while implementation is near zero. |
| **A real maturity spectrum** | The **Governance Maturity** score (how far each mechanism has travelled: strategy → bill → in force) ranks countries from **Brazil 70 / Vietnam 62 (*Advancing*)** down to **Bangladesh 20 (*Nascent*)** — the trajectory the binary in-force score deliberately flattens. |
| **Divergence from EU risk categories** | **15 of 16 (94%)** use *custom* high-risk classifications rather than the EU's tiers — most often elevating healthcare, financial/mobile-money AI, facial recognition, and agriculture. |

Every score is traceable: implementation indicators cite the instrument behind
them; UNESCO/OECD scores are fact-derived (RAM status, adherence). See
[`docs/scoring_rubric.md`](docs/scoring_rubric.md) and [`METHODOLOGY.md`](METHODOLOGY.md).

---

## How this differs from existing indices

This tracker is **not** another AI-readiness ranking. It measures a distinct
construct, and the contrast with the two most-cited indices is the point
(reference data in [`data/benchmarks.json`](data/benchmarks.json)):

| Index | What it measures | This tracker's difference |
|-------|------------------|----------------------------|
| **Oxford Insights — Government AI Readiness Index** (188 countries) | Government *capacity/readiness to use* AI (government, tech sector, data & infrastructure) | We measure **governance/regulation**, not readiness. The contrast is revealing: India ranks **46th** globally for AI *readiness* yet scores **0/100** on our *in-force* implementation — capacity ≠ enforceable rules. |
| **Global Index on Responsible AI — GIRAI** (138 countries) | Responsible-AI *commitments* across human-rights benchmarks | GIRAI's headline 2024 finding — *"AI governance fails to deliver… critical implementation gaps"* — **independently corroborates this tracker's central thesis** (adoption ≫ implementation). Brazil ranks GIRAI **18th** yet its AI law (PL 2338) is not enacted; South Africa is GIRAI's **top-ranked African country** yet has no AI regulation proposed. |

**What is novel here:** (1) isolating **in-force implementation** — the six
operational mechanisms — separately from policy on paper; (2) the explicit
**adoption–implementation gap** as a headline metric; (3) a **Global-South lens**
that surfaces *divergence* from EU risk categories (agriculture, mobile money,
climate) rather than treating EU conformity as the goal. Each finding is
evidence-coded and reproducible — see [`METHODOLOGY.md`](METHODOLOGY.md).

## Citation

This repository ships a [`CITATION.cff`](CITATION.cff), so GitHub shows a **"Cite
this repository"** button. A versioned **Zenodo DOI** is planned (see Roadmap) to
make the dataset formally citable.

---

## About the Author

**Sana Asif Ahmad** — AI governance researcher with hands-on implementation experience.

- 🎓 **Columbia University SIPA Fellow** (2023-24) — Specialized in AI regulation and governance
- 🇺🇳 **UN Development Coordination Office** — Translated EU AI Act and UNESCO AI Ethics frameworks into governance roadmaps for 7 country offices across 4 regions
- 🔬 **University of Pennsylvania** — Currently researching AI governance frameworks for academic applications
- 💻 **Background** — B.E. Computer Science (Osmania University), M.S. Urban Policy (TISS Mumbai)

This project operationalizes insights from translating global AI frameworks into country-level implementation.

📧 saa2252@columbia.edu

---

## Contributing

Contributions welcome! Especially:
- Country-specific implementation data
- Corrections to existing data
- Translations of national AI strategies

See **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)** for the full guide (evidence
rules, the standards cross-walk, and the move toward multi-coder reliability), and
[docs/coding_worksheet.md](docs/coding_worksheet.md) for the per-country protocol.

---

## Citation

If you use this data in research:

```bibtex
@misc{ahmad2026globalai,
  author = {Ahmad, Sana Asif},
  title = {Global South AI Governance Tracker},
  year = {2026},
  version = {3.0},
  publisher = {GitHub},
  url = {https://github.com/Saa2252/ai-governance-tracker},
  note = {DOI to be assigned via Zenodo}
}
```

---

## Responsible use & governance

**What the scores are — and are not.** A score describes the **alignment and
in-force status** of a country's AI-governance *mechanisms* at a point in time. A
low or early-stage score means rules are *not yet enacted or operational* — it is
**not** a verdict on a government's competence, intentions, or sovereignty. Read
"low" as *"early in the pipeline,"* not *"bad."*

**Independent, contestable, versioned.** This is an **independent research project**
(currently a single-coder pilot — see [CONTRIBUTING](docs/CONTRIBUTING.md)), not an
official assessment by any government or international body. Every score is
**evidence-cited and falsifiable**: to contest one, cite a specific in-force
instrument and open an issue. The index audits its own decisions via a public
[CHANGELOG](CHANGELOG.md) and a defined [Update Policy](docs/UPDATE_POLICY.md)
(scheduled + event-triggered re-scoring).

**Toward institutional legitimacy.** Normative scoring of sovereign policy carries
weight once cited. This project therefore actively seeks **peer review, an advisory
board, and partnership** with the bodies it already builds on (UNESCO, OECD). Until
then, cite it as an *independent, methodologically-transparent sample* — not an
authoritative ranking.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Roadmap

- [x] Initial country dataset (16 fully profiled; 24-country roster documented)
- [x] Streamlit dashboard v1
- [x] All 16 countries evidence-coded (every indicator cited)
- [x] Automated World Bank data refresh (scheduled GitHub Action — see [docs/data_pipeline.md](docs/data_pipeline.md))
- [x] Governance Maturity index + robustness/sensitivity validation (ρ = 0.99)
- [x] Public [CHANGELOG](CHANGELOG.md), [Update Policy](docs/UPDATE_POLICY.md) + [watchlist](data/watchlist.json), and a quarterly review-reminder Action
- [ ] Zenodo DOI + tagged release (formal citability)
- [ ] External-validation correlation vs. Oxford Insights & GIRAI (fuller scores)
- [ ] Advisory board / peer review / institutional partnership
- [ ] Auto-pull OECD adherence + UNESCO RAM status
- [ ] Integration with EU AI Act compliance tools

---

*Last updated: May 2026*
