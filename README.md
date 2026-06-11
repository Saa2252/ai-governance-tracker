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
├── METHODOLOGY.md            # Data collection approach
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── data/
│   ├── countries.json        # Full profiles (8 countries)
│   ├── country_roster.json   # Comprehensive in-scope roster (24) + selection logic
│   ├── frameworks.json       # Framework definitions (EU AI Act, UNESCO, etc.)
│   └── risk_categories.json  # How countries classify AI risk vs. the EU baseline
├── app/
│   └── dashboard.py          # Streamlit interactive dashboard
└── docs/
    └── data_dictionary.md    # Plain-English definition of every data field

# Planned (not yet added):
#   analysis/implementation_gaps.ipynb – Jupyter notebook analysis
#   docs/CONTRIBUTING.md                – contribution guidelines
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
| **Divergence from EU risk categories** | **15 of 16 (94%)** use *custom* high-risk classifications rather than the EU's tiers — most often elevating healthcare, financial/mobile-money AI, facial recognition, and agriculture. |

Every score is traceable: implementation indicators cite the instrument behind
them; UNESCO/OECD scores are fact-derived (RAM status, adherence). See
[`docs/scoring_rubric.md`](docs/scoring_rubric.md) and [`METHODOLOGY.md`](METHODOLOGY.md).

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

Contribution guidelines (`docs/CONTRIBUTING.md`) are coming soon. In the
meantime, please open an issue or pull request, and see
[docs/data_dictionary.md](docs/data_dictionary.md) for the data format.

---

## Citation

If you use this data in research:

```bibtex
@misc{ahmad2026globalai,
  author = {Ahmad, Sana Asif},
  title = {Global South AI Governance Tracker},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/Saa2252/ai-governance-tracker}
}
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Roadmap

- [x] Initial country dataset (16 fully profiled; 24-country roster documented)
- [x] Streamlit dashboard v1
- [ ] API endpoint for data access
- [ ] Integration with EU AI Act compliance tools
- [ ] Real-time policy update monitoring

---

*Last updated: May 2026*
