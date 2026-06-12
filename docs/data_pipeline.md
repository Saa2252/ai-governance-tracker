# Data Pipeline & Freshness

How each field stays current — and an honest note on what can and cannot be
automated.

## Three layers

| Layer | Fields | How it updates | Cadence |
|-------|--------|----------------|---------|
| **1. Automated (API)** | internet penetration, population, income group | `scripts/refresh_world_bank.py` via the **World Bank API**, run by a GitHub Action | Weekly (Mondays), or on demand |
| **2. Assisted** | UNESCO RAM status, OECD adherence | Human checks the official observatories when flagged; values are fact-derived | When sources change |
| **3. Manual (verified)** | the six in-force implementation indicators, EU AI Act adoption | Human reads the law/bill/tracker and cites it; see `coding_worksheet.md` | On policy change |

## Why governance scores are **not** auto-scraped

The implementation and adoption scores depend on a qualitative judgement —
*"is this mechanism actually in force, or just proposed?"* — that lives in PDFs,
bills, and news, not in any API. Auto-generating these from "country websites"
would produce confident-looking but unverifiable numbers, which is the opposite of
what an index needs. Their credibility comes from **cited human verification**
(`source` + `as_of` on every indicator). So we automate the facts and keep the
judgement human and traceable.

## Layer 1 — how it works

- **`scripts/refresh_world_bank.py`** pulls the latest World Bank values, updates
  only the three quantitative fields, validates the JSON, and rewrites the file
  *only if something changed*. It never edits governance scores or evidence.
- **`.github/workflows/refresh-data.yml`** runs that script on GitHub's servers
  every Monday (and via a manual "Run workflow" button), then commits any updates
  as `chore(data): auto-refresh World Bank indicators`. No laptop required.

Run it yourself any time:

```bash
python scripts/refresh_world_bank.py
```

## Roadmap for more automation

- Pull OECD AI Principles adherents directly from OECD.AI (Layer 1 → adherence).
- A "watchlist" that diffs the IAPP / OECD.AI trackers and opens an issue when a
  tracked country's status changes (Layer 2 trigger).

*Last updated: 2026-06-10*
