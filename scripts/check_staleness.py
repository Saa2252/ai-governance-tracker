"""
Flag countries whose scores are older than the review window (see
docs/UPDATE_POLICY.md). Used by .github/workflows/review-reminder.yml.

Writes a markdown report to review_report.md, prints it, and sets the
`stale_count` GitHub Actions output. Standard library only; always exits 0.
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

    if stale:
        lines = [f"### {len(stale)} countries due for review "
                 f"(scores older than {WINDOW_DAYS // 30} months)\n",
                 "Per docs/UPDATE_POLICY.md, re-verify these and log any change in CHANGELOG.md.\n"]
        for name, d, age in sorted(stale, key=lambda t: -t[2]):
            lines.append(f"- **{name}** — last verified {d} ({age} days ago)")
        report = "\n".join(lines)
    else:
        report = "All countries are within the 6-month review window. Nothing due."

    Path("review_report.md").write_text(report + "\n")
    print(report)

    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write(f"stale_count={len(stale)}\n")


if __name__ == "__main__":
    main()
