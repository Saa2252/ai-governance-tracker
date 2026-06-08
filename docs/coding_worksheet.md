# Country Coding Worksheet

A repeatable, ~30-minute protocol to promote one country from `provisional` to
`evidence_coded`. No special skills needed — answer six yes/no questions from
reliable sources, then record the answers.

---

## The Golden Rule

> Mark an indicator **`true` only if the mechanism is OPERATIONAL and IN FORCE today.**
> A *draft bill*, a *voluntary guideline*, a *proposed* body, or a strategy that
> *"plans to create"* something = **`false`**.

This strictness is the whole point: it separates governance on paper from
governance in practice.

---

## Step 1 — Answer the six questions

For the country, find evidence for each. Write the answer (yes/no), one sentence
of proof, and the link you found it in.

| # | Indicator (JSON field) | Ask yourself… | Counts as `true` only if… |
|---|------------------------|---------------|----------------------------|
| 1 | `has_enforcement_body` | Is there a government body **actually operating** with a mandate to oversee/enforce AI rules? | The authority exists and is functioning now (not "to be established"). |
| 2 | `has_regulatory_sandbox` | Is there a **live** AI testing/regulatory sandbox? | It is operational and accepting participants. |
| 3 | `has_impact_assessments` | Are AI impact assessments **legally required** for some uses? | A law/regulation in force mandates them. |
| 4 | `has_transparency_requirements` | Are there **binding** AI disclosure rules (e.g. labelling AI content, informing users)? | In force, not voluntary. |
| 5 | `has_audit_mechanisms` | Are **third-party AI audits** required by a rule in force? | Mandatory audit provision exists. |
| 6 | `has_redress_mechanisms` | Can an affected person use an **AI-specific** channel to complain / seek remedy? | A statutory AI redress route is in force. |

## Step 2 — Where to look (free, reliable sources)

Check 2–3 of these for the country; they usually answer all six questions:

- **White & Case "AI Watch: Global regulatory tracker"** — per-country pages, very current
- **OECD.AI Policy Observatory** — `oecd.ai/en/dashboards/national` (official policy list)
- **IAPP Global AI Governance** — `iapp.org` country articles
- **DLA Piper / CMS / Bowmans law-firm AI guides** — clear "is it in force?" summaries
- The **government's own** AI strategy / ministry page (primary source)
- A recent **news article** confirming a body or law is *operational* (not just announced)

## Step 3 — Record it in `data/countries.json`

Find the country block. Make exactly these edits (one country at a time):

1. Set each of the six `has_…` values to `true`/`false` per your findings.
   *(You don't touch `overall_score` — the app recalculates it automatically.)*
2. Change `"coding_status": "provisional"` → `"coding_status": "evidence_coded"`.
3. Add an `evidence` block right after `coding_status`, using this template
   (copy from an already-coded country like Brazil/India/Kenya and edit):

```json
"evidence": {
  "has_enforcement_body":        {"value": false, "as_of": "2026-06", "evidence": "…one sentence…", "source": "https://…"},
  "has_regulatory_sandbox":      {"value": false, "as_of": "2026-06", "evidence": "…", "source": "https://…"},
  "has_impact_assessments":      {"value": false, "as_of": "2026-06", "evidence": "…", "source": "https://…"},
  "has_transparency_requirements":{"value": false,"as_of": "2026-06", "evidence": "…", "source": "https://…"},
  "has_audit_mechanisms":        {"value": false, "as_of": "2026-06", "evidence": "…", "source": "https://…"},
  "has_redress_mechanisms":      {"value": false, "as_of": "2026-06", "evidence": "…", "source": "https://…"}
}
```

4. Make sure each `evidence` `value` matches the `has_…` boolean above it.

## Step 4 — Check it didn't break

Before committing, paste the whole file into **jsonlint.com** → "Validate JSON".
If it says *valid*, you're good. (A red error usually means a missing comma or quote.)

---

## Worked example — Brazil (already coded)

Research found PL 2338 **not yet enacted**, only an ANPD sandbox operational:

| Indicator | Value | One-line evidence |
|-----------|-------|-------------------|
| Enforcement body | false | PL 2338 still in Chamber of Deputies; SIA not in force |
| Regulatory sandbox | **true** | ANPD ran a pilot AI + data-protection sandbox |
| Impact assessments | false | Mandated by PL 2338, but bill not in force |
| Transparency | false | Depends on PL 2338, not yet law |
| Audit | false | No in-force AI audit requirement |
| Redress | false | Depends on PL 2338 |

→ Score auto-calculates to **20** (sandbox only). See Brazil's `evidence` block in
`countries.json` for the exact JSON to mimic.

---

## Suggested coding order (one per session)

High-traffic first, then the rest:

1. Mexico  2. South Africa  3. Nigeria  4. Indonesia  5. Bangladesh
6. Pakistan  7. Vietnam  8. Philippines  9. Thailand  10. Malaysia
11. Argentina  12. Colombia  13. Sri Lanka

When all 13 are done, the whole index is `evidence_coded` — a complete,
defensible, citation-ready product.

*Last updated: 2026-06-08*
