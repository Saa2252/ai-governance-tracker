#!/usr/bin/env python3
"""
Auto-refresh the World Bank-sourced (quantitative) fields in data/countries.json.

Updates only:
  - digital_context.internet_penetration_pct / _year   (indicator IT.NET.USER.ZS)
  - population_millions                                 (indicator SP.POP.TOTL)
  - income_level                                        (World Bank income group)

It NEVER touches governance scores, framework alignment, or evidence — those are
human-verified and cited. Standard library only (runs anywhere, no pip install).
Writes the file only if something actually changed.

Usage:  python scripts/refresh_world_bank.py
"""
import datetime
import json
import urllib.error
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "countries.json"
API = "https://api.worldbank.org/v2"
INCOME_MAP = {"LIC": "low", "LMC": "lower_middle", "UMC": "upper_middle", "HIC": "high_income"}
NET_SOURCE = "World Bank, Individuals using the Internet (% of population), indicator IT.NET.USER.ZS"


def _fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ai-governance-tracker"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def latest_indicator(codes, indicator):
    """{ISO3: (value, year)} most-recent non-empty value for an indicator."""
    url = f"{API}/country/{';'.join(codes)}/indicator/{indicator}?format=json&mrnev=1&per_page=1000"
    payload = _fetch(url)
    out = {}
    if len(payload) < 2 or not payload[1]:
        return out
    for row in payload[1]:
        code, value, year = row.get("countryiso3code"), row.get("value"), row.get("date")
        if value is not None and code and code not in out:
            out[code] = (value, int(year))
    return out


def income_levels(codes):
    """{ISO3: income_level} from the World Bank country metadata."""
    url = f"{API}/country/{';'.join(codes)}?format=json&per_page=1000"
    payload = _fetch(url)
    out = {}
    if len(payload) >= 2 and payload[1]:
        for row in payload[1]:
            out[row["id"]] = INCOME_MAP.get((row.get("incomeLevel") or {}).get("id"))
    return out


def main():
    doc = json.loads(DATA.read_text())
    codes = [c["country_code"] for c in doc["countries"]]

    try:
        net = latest_indicator(codes, "IT.NET.USER.ZS")
        pop = latest_indicator(codes, "SP.POP.TOTL")
        inc = income_levels(codes)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"World Bank API unavailable ({exc}). No changes made.")
        return 0

    changes = 0
    for c in doc["countries"]:
        code = c["country_code"]
        dc = c.setdefault("digital_context", {})

        if code in net:
            value, year = round(net[code][0], 1), net[code][1]
            if dc.get("internet_penetration_pct") != value or dc.get("internet_penetration_year") != year:
                dc["internet_penetration_pct"] = value
                dc["internet_penetration_year"] = year
                dc["internet_penetration_source"] = NET_SOURCE
                print(f"  {c['country_name']}: internet -> {value}% ({year})")
                changes += 1

        if code in pop:
            millions = round(pop[code][0] / 1_000_000)
            if c.get("population_millions") != millions:
                print(f"  {c['country_name']}: population -> {millions}M")
                c["population_millions"] = millions
                changes += 1

        if inc.get(code) and c.get("income_level") != inc[code]:
            print(f"  {c['country_name']}: income_level -> {inc[code]}")
            c["income_level"] = inc[code]
            changes += 1

    if changes:
        doc.setdefault("metadata", {})["last_updated"] = datetime.date.today().isoformat()
        DATA.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"\nUpdated {changes} field(s). data/countries.json rewritten.")
    else:
        print("No changes — World Bank figures already current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
