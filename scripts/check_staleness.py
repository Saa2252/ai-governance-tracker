"""
Free, no-cost reminder (no API key). Two checks, see docs/UPDATE_POLICY.md:
  1. Countries whose scores are older than the 6-month review window.
  2. Watch-list events (data/watchlist.json) whose expected date has arrived —
     i.e. a tracked law/bill is due, so go verify whether it passed.

Used by .github/workflows/review-reminder.yml. Writes review_report.md, prints it,
and sets the `stale_count` GitHub Actions output. Standard library only; exits 0.
"""
import datetime
import json
import os
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
WINDOW_DAYS = 183  # ~6 months


def _parse(d):
    if not d:
        return None
    try:
        return datetime.date.fromisoformat(d if len(d) == 10 else d + "-01")
    except ValueError:
        return None


def oldest_date(country):
    dates = [_parse(country.get("data_quality", {}).get("last_verified"))]
    for ev in country.get("implementation_status", {}).get("evidence", {}).values():
        dates.append(_parse(ev.get("as_of")))
    dates = [d for d in dates if d]
    return min(dates) if dates else None


def due_watchlist_events(today):
    """Watch-list events whose expected period has arrived (year <= this year)."""
    wl_path = DATA / "watchlist.json"
    if not wl_path.exists():
        return []
    due = []
    for e in json.loads(wl_path.read_text()).get("events", []):
        if e.get("status") != "pending":
            continue
        exp = str(e.get("expected", ""))
        # expected like "2026", "2026-08", "2026-2027" -> take the first year
        years = [int(y) for y in exp.replace("-", " ").split() if y.isdigit() and len(y) == 4]
        if years and min(years) <= today.year:
            due.append(e)
    return due


def main():
    rows = json.loads((DATA / "countries.json").read_text())["countries"]
    comp = DATA / "comparators_developed.json"
    if comp.exists():
        rows += json.loads(comp.read_text())["countries"]

    today = datetime.date.today()

    stale = []
    for c in rows:
        d = oldest_date(c)
        if d and (today - d).days > WINDOW_DAYS:
            stale.append((c["country_name"], d.isoformat(), (today - d).days))

    due = due_watchlist_events(today)

    sections = []
    if due:
        s = [f"### {len(due)} watch-list events due — a tracked law may have passed\n",
             "Check whether each has happened; if so, re-score within 4 weeks and log it in CHANGELOG.md.\n"]
        for e in due:
            s.append(f"- **{e['country_code']}** — {e['event']} (expected {e['expected']}) → {e['trigger']}")
        sections.append("\n".join(s))
    if stale:
        s = [f"### {len(stale)} countries due for review (scores older than {WINDOW_DAYS // 30} months)\n"]
        for name, d, age in sorted(stale, key=lambda t: -t[2]):
            s.append(f"- **{name}** — last verified {d} ({age} days ago)")
        sections.append("\n".join(s))

    report = "\n\n".join(sections) if sections else \
        "Nothing due: no watch-list events have arrived and all scores are within the 6-month window."

    Path("review_report.md").write_text(report + "\n")
    print(report)

    total_due = len(due) + len(stale)
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write(f"stale_count={total_due}\n")


if __name__ == "__main__":
    main()
