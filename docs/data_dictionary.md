# Data Dictionary

Plain-English definition of every field in `data/countries.json`. This is the
companion reference for anyone reading, reusing, or contributing to the dataset.

**Schema version:** 1.1
**File:** `data/countries.json`

---

## How the file is organised

The file has two top-level parts:

- **`metadata`** — information *about the dataset* (version, when it was updated, who made it).
- **`countries`** — a list, where each entry is one country with all the fields below.

---

## `metadata`

| Field | Plain meaning |
|---|---|
| `version` | Schema version of the dataset (e.g. `"1.1"`). Bumped when fields change. |
| `last_updated` | Date the dataset as a whole was last edited (`YYYY-MM-DD`). |
| `author` | Person responsible for the data. |
| `description` | One line describing what the dataset covers. |
| `data_sources` | The broad categories of evidence the data is drawn from. |
| `schema_note` | Short note on what changed in the latest schema version. |

---

## Per-country fields

### Basic identity

| Field | Plain meaning | Example |
|---|---|---|
| `country_code` | 3-letter ISO country code. | `"IND"` |
| `country_name` | Full country name. | `"India"` |
| `region` | World region used for grouping. | `"South Asia"` |
| `income_level` | World Bank income band: `low`, `lower_middle`, `upper_middle`, `high`. | `"lower_middle"` |
| `population_millions` | Population in millions. | `1428` |

### `ai_strategy` — does the country have a national AI plan?

| Field | Plain meaning |
|---|---|
| `has_national_strategy` | `true`/`false` — is there an official national AI strategy? |
| `strategy_name` | The document's name. |
| `year_published` | Year the strategy was first published. |
| `year_updated` | Year of the most recent update (`null` if never updated). |
| `lead_agency` | Government body in charge of it. |

### `framework_alignment` — how closely the country follows each international rulebook

Contains one block per framework (`eu_ai_act`, `unesco_ai_ethics`, `oecd_ai_principles`).
Each block has:

| Field | Plain meaning |
|---|---|
| `adoption_status` | Short label for the relationship (see vocabulary note below). |
| `adoption_score` | 0–100 score for how closely the country aligns. Scored via [`scoring_rubric.md`](scoring_rubric.md). |
| `notes` | Free-text explanation of the score. |
| `source` | *(v1.4)* Citation for the score: `primary_instrument` (the policy/law it rests on), `framework_reference_url` (the framework text), and `verify_via` (OECD.AI lookup). |
| `evidence` | *(v2.1)* Fact basis for the score. **OECD:** `oecd_member`, `ai_principles_adherent`, `gpai_member`. **UNESCO:** `adopted_2021_recommendation`, `ram_status` (`completed`/`in_progress`/`not_confirmed`). Each with `as_of` + `source`. |

> **Vocabulary note:** `adoption_status` currently mixes several word-sets
> (`partial`, `endorsed`, `aligned`, `high`, `member`, `observer`, `partner`,
> `none`). For cleaner filtering, the **recommended standard vocabulary** is:
> `none` · `low` · `partial` · `high` · `endorsed` · `member`. Treat
> membership/observer/partner as descriptors of OECD *relationship* and prefer
> recording those under `international_engagement.oecd_status` (below).

### `implementation_status` — is it real, or just on paper?

Mirrors the six scoring components in `METHODOLOGY.md`.

| Field | Plain meaning |
|---|---|
| `overall_score` | 0–100 weighted implementation score. |
| `has_enforcement_body` | A designated authority with an AI mandate exists. |
| `has_regulatory_sandbox` | An operational testing environment for AI exists. |
| `has_impact_assessments` | AI impact assessments are required. |
| `has_transparency_requirements` | Disclosure obligations exist. |
| `has_audit_mechanisms` | Third-party audit provisions exist. *(added in v1.1)* |
| `has_redress_mechanisms` | Channels for people to seek remedy exist. *(added in v1.1)* |
| `coding_status` | *(v2.0)* `evidence_coded` (every indicator researched + cited; defensible) or `provisional` (unverified estimate). |
| `evidence` | *(v2.0, evidence-coded countries only)* Per-indicator record: `value`, `as_of` date, one-line `evidence`, and `source` URL. |

> **`overall_score` is deterministic (v2.0):** it equals the weighted sum of the six
> booleans (25/20/20/15/10/10) where each is `1` only if the mechanism is *operational
> and in force*. `analysis/findings.py` asserts this for every country.

### `risk_classification` — how the country defines "risky" AI

| Field | Plain meaning |
|---|---|
| `uses_eu_categories` | Does it use the EU's risk tiers, or its own? |
| `custom_high_risk` | List of AI uses the country treats as high-risk. |
| `divergence_notes` | How its view differs from the EU framework. |

### `key_developments` — timeline

A list of `{ "date": "YYYY-MM", "event": "..." }` milestones.

### `digital_context` — the groundwork needed to enforce AI rules *(new in v1.1)*

| Field | Plain meaning |
|---|---|
| `internet_penetration_pct` | % of population using the internet. **Sourced** — see the two fields below. |
| `internet_penetration_year` | Year of that figure. |
| `internet_penetration_source` | Citation for the figure (World Bank indicator IT.NET.USER.ZS). |
| `has_data_protection_law` | `true`/`false` — is there an *enacted* privacy/data law? AI rules usually sit on top of one. |
| `data_protection_law_name` | Name of that law (or the draft, if not yet enacted). |
| `ai_talent_availability` | `low` / `medium` / `high` — rough local skills/research capacity *(estimate)*. |

### `priority_sectors` — where the country focuses AI governance *(new in v1.1)*

A list of economic sectors (e.g. agriculture, fintech, mining). Previously this
lived only inside narrative notes; now it is a searchable field.

### `international_engagement` — the country's seat at global tables *(new in v1.1)*

| Field | Plain meaning |
|---|---|
| `oecd_status` | `member` · `acceding` · `adherent` · `non_member`. |
| `gpai_member` | `true`/`false` — member of the Global Partnership on AI. |
| `signatory_coe_ai_convention` | `true`/`false` — signed the Council of Europe AI Convention. |

### `inclusion` — who had a voice, and who is protected *(new in v1.1)*

| Field | Plain meaning |
|---|---|
| `public_consultation_held` | Was the public consulted on the AI policy? |
| `civil_society_involved` | Were civil-society / advocacy groups involved? |
| `gender_or_inclusion_provisions` | Does the policy include explicit equity/inclusion provisions? |

### `data_quality` — how much to trust each country entry *(new in v1.1)*

| Field | Plain meaning |
|---|---|
| `last_verified` | Date this country's entry was last checked (`YYYY-MM-DD`). |
| `confidence_level` | `high` / `medium` / `low` — honest signal of how solid the entry is. |
| `sources` | The specific documents this entry draws on. |
| `verified_fields` | Fields cross-checked against authoritative external sources (treat as citation-ready). |
| `illustrative_fields` | Fields that are researcher estimates / scores, **not** yet citation-ready. |

---

## Companion file: `data/country_roster.json`

The comprehensive list of every country in scope, plus the **verifiable logic**
for why each is in or out.

| Section | Plain meaning |
|---|---|
| `selection_criteria` | The three tests a country must pass to be in scope (income, region, governance-to-track) and how each is verified. |
| `summary` | Counts: in-scope total, fully profiled, and roster-only awaiting profiling. |
| `roster` | Every in-scope country with its World Bank income group, AI-strategy status, `meets_criteria`, and `fully_profiled` flags. |
| `excluded_examples` | Borderline countries (e.g. Chile, Singapore) shown *with the reason they fail*, to demonstrate the logic. |

Roster row fields: `country_code`, `country_name`, `region`,
`income_level_worldbank`, `national_ai_strategy` (`published`/`draft`/`in_development`/`none`),
`meets_criteria` (bool), `fully_profiled` (bool — `true` means it has a full record in `countries.json`).

---

## Companion file: `data/risk_categories.json`

A standalone reference for how "risky" AI is classified. Three sections:

| Section | Plain meaning |
|---|---|
| `reference_taxonomy` | The EU AI Act's four risk tiers (the yardstick everything is measured against), each with its obligations. |
| `global_south_divergences` | Recurring themes where tracked countries treat a sector as higher-risk than the EU does (e.g. agriculture, mobile money), with the list of countries that do so. |
| `country_risk_profiles` | Each country's own high-risk list, kept in sync with `countries.json`. |

---

## Other companion files

| File | Purpose |
|---|---|
| [`scoring_rubric.md`](scoring_rubric.md) | The rubric behind every score, with high/mid/low worked examples (evidence → number). |
| [`../analysis/findings.py`](../analysis/findings.py) | Reproduces all README headline statistics from `countries.json` (standard library only). |
| `../data/comparators_developed.json` | **Optional overlay** (feature branch): high-income comparator countries (Germany, France, UK, US, Japan, South Korea, Canada, Australia). Same schema; *not* part of the core Global South dataset. |

## Field types at a glance

- **Boolean** (`true`/`false`): all `has_*` fields, `uses_eu_categories`, the `inclusion` fields, `gpai_member`, `signatory_coe_ai_convention`, `has_national_strategy`.
- **Number**: `adoption_score`, `overall_score` (0–100); `population_millions`; `internet_penetration_pct`; year fields.
- **Controlled text** (fixed set of allowed values): `income_level`, `ai_talent_availability`, `oecd_status`, `confidence_level`, `adoption_status`.
- **Free text / lists**: everything else.

*Last updated: 2026-05-30*
