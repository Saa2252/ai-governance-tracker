# Methodology

## Country Selection

The full roster and the machine-readable version of this logic live in
[`data/country_roster.json`](data/country_roster.json). A country is **in scope**
only if it meets **all three** verifiable criteria:

| # | Criterion | How it is verified |
|---|-----------|--------------------|
| 1 | **Income** — World Bank income group is low, lower-middle, or upper-middle (i.e., *not* high-income). | World Bank country & lending groups (updated each July). |
| 2 | **Region** — located in a Global South region: Sub-Saharan Africa, North Africa & MENA, South Asia, Southeast Asia, Central Asia, Latin America & Caribbean, or Pacific Islands. | UN M49 standard regional classification. |
| 3 | **Governance to track** — has a national AI strategy that is published, drafted, or in formal development, *or* has endorsed a regional AI framework (AU / ASEAN). | OECD.AI Policy Observatory. |

**Why not "G77 membership" as the proxy?** It would wrongly exclude Mexico (not a
G77 member) even though Mexico is clearly in scope. Income + UN region is cleaner
and fully reproducible. High-income peers with strong AI policies — Chile, Uruguay,
Singapore, the Gulf states — are deliberately **excluded** (see `excluded_examples`
in the roster file) because the tracker is about *developing economies*.

**Which countries get a full profile first?** Among in-scope countries, full
profiling (a complete record in `countries.json`) is prioritised by: (1) regional
coverage — at least one country per region; (2) population weight; (3) availability
of primary-source data from UN DCO country offices. This is why the initial 8 span
South Asia, Southeast Asia, Sub-Saharan Africa, and Latin America. The remaining
in-scope countries sit in the roster as candidates awaiting full profiling.

## Data Collection Approach

This tracker combines primary research from field implementation with secondary analysis of official documents.

### Primary Sources

**UN Development Coordination Office (2025)**
- Policy implementation data from 7 country offices across 4 regions
- Insights from translating EU AI Act and UNESCO AI Ethics frameworks into country-level governance roadmaps
- Interviews with 15 senior UN officials on implementation challenges

**National AI Strategies**
- Official government documents from 50+ countries
- Analysis of strategy text for framework alignment
- Comparison of stated priorities vs. EU AI Act categories

**Regulatory Filings**
- Draft and enacted AI legislation
- Public consultation documents
- Regulatory impact assessments where available

### Scoring Methodology

#### Framework Adoption Score (0-100)

Measures how closely a country's policies align with a given framework:

| Score Range | Classification | Criteria |
|-------------|----------------|----------|
| 80-100 | High | Direct adoption or very close alignment |
| 50-79 | Partial | Selective adoption; some provisions modified |
| 20-49 | Low | Limited alignment; framework referenced only |
| 0-19 | None | No meaningful alignment |

#### Implementation Score (0-100)

Measures actual operationalization of governance:

| Component | Weight | Criteria |
|-----------|--------|----------|
| Enforcement body | 25 | Designated authority with AI mandate |
| Regulatory sandbox | 20 | Operational sandbox for AI testing |
| Impact assessments | 20 | Mandatory AI impact assessments |
| Transparency requirements | 15 | Disclosure obligations |
| Audit mechanisms | 10 | Third-party audit provisions |
| Redress mechanisms | 10 | Channels for remedy |

### Limitations

1. Language barriers in accessing some national strategies
2. Implementation lag: policy doesn't equal enforcement
3. Rapid change: data may lag recent developments

---

*Last updated: May 2026*
