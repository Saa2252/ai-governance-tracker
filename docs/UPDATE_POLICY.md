# Update Policy — re-scoring cadence & triggers

A credible index re-scores on a **defined schedule** and in response to **real
regulatory events** — not via an ad-hoc "last updated" note. This is that policy.

## 1. Scheduled review

- **Quarterly review.** A country is flagged for review when its
  `data_quality.last_verified` (or any indicator `as_of`) is older than **6 months**.
  An automated check — [`scripts/check_staleness.py`](../scripts/check_staleness.py),
  run by [`.github/workflows/review-reminder.yml`](../.github/workflows/review-reminder.yml)
  — opens a GitHub issue listing exactly what is due.
- **Annual (July).** Refresh World Bank income groups. (Internet % and population are
  already auto-refreshed weekly — see [`data_pipeline.md`](data_pipeline.md).)

## 2. Event-triggered re-scoring

When a **tracked regulatory event** fires (see [`data/watchlist.json`](../data/watchlist.json)),
the affected country is re-scored **within 4 weeks**, with a `CHANGELOG.md` entry.
Trigger events include:

- A national AI **law/bill is enacted or enters into force** → move the relevant
  mechanism from stage 2 (*drafted*) to stage 3 (*in force*).
- An **enforcement authority becomes operational** → `enforcement_body` in force.
- A **sandbox** opens, or **impact assessments / transparency / audit / redress**
  come into force → re-score that mechanism.
- A **framework milestone** (e.g. EU AI Act high-risk obligations, Aug 2026).

## 3. How a change is recorded (the index's own audit trail)

Every re-score must:
1. Update the indicator's `evidence`, `as_of`, and `source`.
2. Add a `CHANGELOG.md` line: **old → new** value + the reason.
3. Bump `metadata.version`.

This makes each of the index's *own* decisions as auditable as the country
enforcement it measures.

## 4. The watchlist

[`data/watchlist.json`](../data/watchlist.json) lists pending events with expected
dates and the **exact trigger condition**, so a reviewer knows what to watch and
precisely what to change when it fires.

*Last updated: 2026-06.*
