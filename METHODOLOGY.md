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

## Why the EU AI Act Is the Baseline

The tracker measures every country against the **EU AI Act** as its primary
yardstick. This is a deliberate analytical choice, not a claim that the EU model
is "best." The reasons:

1. **It is the only comprehensive, binding, horizontal AI law in force.** UNESCO,
   OECD, AU, and ASEAN instruments are principles or guidelines (soft law); the
   EU AI Act is enforceable hard law with penalties. A baseline needs to be
   concrete and measurable — vague principles can't be scored consistently.
2. **It is the de-facto global reference point ("Brussels Effect").** Because the
   Act applies to any AI system placed on the EU market, exporters worldwide must
   reckon with it, and many national bills (e.g. Brazil's PL 2338, Colombia's
   draft) explicitly mirror its structure. Tracking alignment to it captures real
   regulatory pressure that countries actually respond to.
3. **Its risk-tier structure is operationalisable.** The four tiers
   (unacceptable / high / limited / minimal) give clear, comparable checkpoints,
   which is what lets us compare a Kenyan and a Mexican approach on the same axis.

**Important caveat (also surfaced in the dashboard):** using the EU Act as the
baseline does *not* imply Global South countries *should* simply copy it. A core
finding of this tracker is precisely where local priorities (agriculture, mobile
money, climate) justify *diverging* from EU categories. The baseline is a common
ruler for comparison, not a prescription. We pair every adoption score with the
UNESCO and OECD scores so no single framework dominates the picture.

## Measuring the "Gap"

The headline metric is the **Adoption–Implementation Gap**:

```
Gap = EU AI Act Adoption Score  −  Implementation Score
```

- **Adoption Score (0–100)** = how closely a country's *written policy* aligns
  with the EU AI Act (see scale below). High = the rules exist on paper.
- **Implementation Score (0–100)** = how much of that is *actually operational* —
  enforcement body, sandbox, impact assessments, transparency, audit, redress
  (weighted; see below). High = the rules are real.
- **A large positive gap** means a country has written ambitious AI policy but has
  not yet built the machinery to enforce it ("policy ahead of practice"). A small
  or negative gap means policy and enforcement are roughly in step.

Worked example: India scores ~45 on EU AI Act adoption but ~40 on implementation,
a modest gap; a country that endorses frameworks rhetorically but builds no
enforcement body would show a much wider gap. The gap is the single number that
exposes "governance theatre" versus genuine capacity.

### Scoring Methodology

#### Framework Adoption Score (0-100)

Measures how closely a country's policies align with a given framework:

| Score Range | Classification | Criteria |
|-------------|----------------|----------|
| 80-100 | High | Direct adoption or very close alignment |
| 50-79 | Partial | Selective adoption; some provisions modified |
| 20-49 | Low | Limited alignment; framework referenced only |
| 0-19 | None | No meaningful alignment |

The **EU AI Act** adoption score is expert-coded against this rubric (and
source-cited). The **UNESCO** and **OECD** scores are *fact-derived* (see below).

#### Fact-derived UNESCO & OECD scores (v2.1)

Unlike the EU score, the UNESCO and OECD scores are computed from **verifiable
membership/participation data**, each with an `evidence` record:

**OECD AI Principles** — anchored to the official adherents list, OECD membership,
and GPAI membership:

| Status (verifiable) | Score |
|---------------------|------:|
| OECD member (and adherent) | 85 |
| Formal non-member adherent (e.g. Brazil, Argentina) | 75 |
| GPAI member / OECD accession underway | 55 |
| OECD partner, references principles | 45 |
| References only / minimal | 20–40 |

**UNESCO Ethics** — anchored to adoption of the 2021 Recommendation (universal
among UNESCO members) plus **Readiness Assessment Methodology (RAM)** status:

| Status (verifiable) | Score |
|---------------------|------:|
| Adopted Recommendation + **completed RAM** | 70 |
| Adopted + RAM consultation underway | 55 |
| Adopted Recommendation only (RAM not confirmed) | 45 |

Sources: OECD.AI AI Principles page; UNESCO Global AI Ethics & Governance
Observatory (RAM). RAM status marked `not_confirmed` is honestly flagged pending
per-country verification on the UNESCO observatory.

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

#### Deterministic aggregation (v2.0)

The Implementation Score is **not** a subjective judgement — it is the exact
weighted sum of the six indicators above:

```
Implementation Score = 25·enforcement + 20·sandbox + 20·impact_assessment
                     + 15·transparency + 10·audit + 10·redress
```

where each indicator is **1 only if the mechanism is operational and in force**,
and **0 if it is merely proposed, drafted, or voluntary**. This makes every score
reconstructable from first principles and machine-verifiable
(`analysis/findings.py` asserts `score == weighted_sum` for all countries). The
strict "in force" threshold is deliberate: it is what separates *governance on
paper* from *governance in practice*.

#### Evidence coding & verification status

Each indicator carries an `evidence` record (the value, an `as_of` date, a
one-line justification, and a source URL). A country is one of:

| `coding_status` | Meaning |
|-----------------|---------|
| `evidence_coded` | Every indicator individually researched and cited. **Defensible / citation-ready.** |
| `provisional` | Indicators are initial expert estimates **not yet** evidence-coded. Treat as an *unverified upper bound* — pilots show estimates typically fall once strictly coded. |

**Current status (v3.0): all 16 countries are fully evidence-coded** — no
provisional implementation scores remain. Strict coding revised most scores toward
zero versus the initial estimates: e.g. Brazil's "national AI authority" is not yet
in force (PL 2338 is still in the Chamber of Deputies), so enforcement scores 0,
not 25. Result: **0 of 16 have an operational AI enforcement body**, and only
Brazil (ANPD sandbox) and Vietnam (in-force content-labelling, 1 March 2026)
register any in-force mechanism.

#### How to contest a score

Every indicator names the instrument it rests on. To challenge one, cite a
*specific, in-force* legal or regulatory instrument (with article/section) that
meets the threshold, and open an issue. The rubric is designed to be falsifiable.

### Governance Maturity Score (0–100)

The Implementation Score is deliberately binary ("in force or not"), which makes
it an honest reality check but a *flat* ranking — almost no country has anything
fully in force, so most score 0. The **Maturity Score** restores discrimination by
scoring how far each mechanism has travelled, on a four-stage scale:

| Stage | Meaning |
|------:|---------|
| 0 | Absent — no mention |
| 1 | Committed — named in a national strategy/policy |
| 2 | Proposed — drafted bill in legislature, guidelines issued, or body announced (not operating) |
| 3 | **Operational / in force** |

Each mechanism contributes `weight × stage/3` (same weights as implementation:
25/20/20/15/10/10), summed to 0–100, and bucketed into **Nascent / Emerging /
Developing / Advancing / Established**. Stages are derived from the *same cited
evidence* as the implementation indicators. A mechanism only reaches stage 3 when
it would also score `true` on the binary Implementation Score — so
**Maturity ≥ Implementation** always, and the two are consistent by construction.

**Read them together:** Implementation answers *"is it real yet?"* (mostly no);
Maturity answers *"how far along is it?"* (a real spectrum — Brazil 70 *Advancing*
to Bangladesh 20 *Nascent*).

### Alignment with global standards (UNESCO RAM & OECD)

The six mechanisms are not ad hoc — each maps to a recognised international
instrument, so the index sits on accepted scaffolding rather than inventing its
own categories:

| Mechanism (this index) | UNESCO RAM dimension | OECD AI Principle |
|------------------------|----------------------|-------------------|
| Enforcement body | Legal & Regulatory | Accountability |
| Regulatory sandbox | Technological & Infrastructural / Economic | Robustness, security & safety |
| Impact assessments | Legal & Regulatory + Social & Cultural | Accountability; human-centred values |
| Transparency requirements | Legal & Regulatory | Transparency & explainability |
| Audit mechanisms | Legal & Regulatory | Accountability; robustness |
| Redress mechanisms | Social & Cultural + Legal & Regulatory | Human-centred values & fairness |

UNESCO RAM = the five dimensions of UNESCO's *Readiness Assessment Methodology*
(Legal & Regulatory, Social & Cultural, Economic, Scientific & Educational,
Technological & Infrastructural). OECD = the five value-based *OECD AI Principles*.
This cross-walk lets the tracker be read alongside, and contributed to by, work
that uses those frameworks.

### Why these six indicators

The six mechanisms are **not invented** — they are the operational obligations the
EU AI Act itself imposes, generalised so any jurisdiction can be scored on them:

| Mechanism | Anchored in |
|-----------|-------------|
| Enforcement body | EU AI Act Art. 70 (national competent authorities) + market surveillance |
| Regulatory sandbox | EU AI Act Arts. 57–59 (AI regulatory sandboxes) |
| Impact assessments | EU AI Act Art. 27 (fundamental-rights impact assessment), Art. 9 (risk management) |
| Transparency | EU AI Act Arts. 13 & 50 (transparency obligations) |
| Audit | EU AI Act Art. 43 (conformity assessment / third-party) |
| Redress | EU AI Act Arts. 85–87 (right to complain / explanation); CoE Framework Convention (remedies) |

So the indicator set is grounded in binding law and the OECD/UNESCO instruments
above, not chosen ad hoc.

### Weighting, aggregation, and imputation

**Weights** (enforcement 25 · sandbox 20 · impact 20 · transparency 15 · audit 10
· redress 10) are an **expert judgement** with a stated rationale: an operating
*enforcement body* is the precondition for the other five (highest weight);
*sandboxes* and *impact assessments* are the primary proactive tools; *audit* and
*redress* are essential but downstream and rarest. They are **not claimed to be
optimal** — see the sensitivity result below.

**Aggregation is compensatory** for Maturity (a high stage on one mechanism offsets
a low one), which suits a *progress* measure. The **in-force count is
non-compensatory** (each mechanism must independently be in force), giving a strict
complementary view. Reporting both is deliberate.

**Imputation (explicit):** where a country's UNESCO `ram_status` is
`not_confirmed`, its UNESCO score is set to 45 ("adopted the 2021 Recommendation
only") — a *conservative* rule (assume no RAM unless confirmed). This affects
**only the UNESCO sub-score** (9 of 16 countries); Maturity and the in-force score
do not use RAM and are unaffected.

### Robustness & validation (reproduce with `analysis/robustness.py`)

- **Multivariate (no redundancy):** Pearson correlations among the six mechanism
  stages range **0.10–0.79**; no pair approaches 1.0. The highest, *audit ↔ redress
  = 0.79*, reflects that those two tend to arrive together — related, not redundant.
- **Weighting sensitivity (rankings are robust):** re-ranking every country under
  **equal weights** vs the weights above gives a **Spearman rank correlation of
  0.99**. The conclusions therefore do **not** depend on the specific weights; the
  most weight-sensitive country shifts by only ~5 points.

These two checks (OECD/JRC steps 4, 6, 7) are what let the Maturity score be read
as an *index* rather than an arbitrary weighting.

### Limitations

1. **Coverage:** 16 countries fully profiled and **all evidence-coded** (v3.0). Expansion to the 24-country roster is future work.
2. **Adoption scores remain expert coding.** Unlike the Implementation Score (deterministic), Framework Adoption is an expert assessment against the rubric bands. It is rubric-anchored and source-cited, but not mechanical; inter-coder reliability testing is future work.
3. **Data vintage:** indicator `as_of` dates and `last_verified` fields record currency. AI policy moves fast; treat any score older than its `as_of` with caution.
4. **Language barriers** in accessing some national strategies.
5. **Implementation lag:** policy does not equal enforcement — which is precisely what the adoption-implementation gap is designed to measure.

---

*Last updated: May 2026*
