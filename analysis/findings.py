"""
Reproduces every headline statistic in the README directly from data/countries.json.

Run from the repo root:   python analysis/findings.py
No third-party dependencies (standard library only).
"""
import json
import statistics as st
from collections import defaultdict, Counter
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "countries.json"


def eu(c):
    return c["framework_alignment"]["eu_ai_act"]["adoption_score"]


def impl(c):
    return c["implementation_status"]["overall_score"]


WEIGHTS = {
    "has_enforcement_body": 25,
    "has_regulatory_sandbox": 20,
    "has_impact_assessments": 20,
    "has_transparency_requirements": 15,
    "has_audit_mechanisms": 10,
    "has_redress_mechanisms": 10,
}


def weighted_sum(impl):
    return sum(w for k, w in WEIGHTS.items() if impl.get(k))


def main():
    countries = json.loads(DATA.read_text())["countries"]
    n = len(countries)
    print(f"Dataset: {n} countries\n")

    # Integrity check: every implementation score must equal its weighted sum.
    bad = [c["country_name"] for c in countries
           if c["implementation_status"]["overall_score"]
           != weighted_sum(c["implementation_status"])]
    print("Implementation determinism check:",
          "PASS (all scores == weighted sum)" if not bad else f"FAIL: {bad}")
    coded = [c["country_name"] for c in countries
             if c["implementation_status"].get("coding_status") == "evidence_coded"]
    print(f"Evidence-coded (citation-ready): {len(coded)}/{n} -> {coded}")
    print(f"Provisional (unverified upper bound): {n - len(coded)}/{n}\n")

    print("--- Descriptive aggregates (all 16 countries evidence-coded) ---\n")
    avg_eu = st.mean(eu(c) for c in countries)
    avg_impl = st.mean(impl(c) for c in countries)
    print("Policy runs ahead of practice")
    print(f"  Avg EU AI Act adoption : {avg_eu:.0f}/100")
    print(f"  Avg implementation     : {avg_impl:.0f}/100")
    print(f"  Average gap            : {avg_eu - avg_impl:.0f} pts")

    enf = sum(c["implementation_status"]["has_enforcement_body"] for c in countries)
    print(f"  Operational enforcement body: {enf}/{n} ({100*enf/n:.0f}%)\n")

    custom = sum(not c["risk_classification"]["uses_eu_categories"] for c in countries)
    print("Divergence from EU risk categories")
    print(f"  Use custom high-risk classes: {custom}/{n} ({100*custom/n:.0f}%)")
    sectors = Counter()
    for c in countries:
        for h in c["risk_classification"]["custom_high_risk"]:
            sectors[h.lower().split(" /")[0].split(" (")[0].strip()] += 1
    print(f"  Most common custom high-risk sectors: "
          f"{', '.join(s for s, _ in sectors.most_common(5))}\n")

    by_income = defaultdict(list)
    for c in countries:
        by_income[c["income_level"]].append(impl(c))
    print("Capacity tracks income (avg implementation)")
    for k, v in by_income.items():
        print(f"  {k:<14}: {st.mean(v):.0f}/100  (n={len(v)})")
    print()

    by_region = defaultdict(list)
    for c in countries:
        by_region[c["region"]].append(eu(c) - impl(c))
    print("Average adoption-implementation gap by region")
    for r, v in sorted(by_region.items(), key=lambda x: -st.mean(x[1])):
        print(f"  {r:<26}: {st.mean(v):.0f} pts  (n={len(v)})")
    widest = max(countries, key=lambda c: eu(c) - impl(c))
    print(f"\nWidest single-country gap: {widest['country_name']} "
          f"({eu(widest)} - {impl(widest)} = {eu(widest) - impl(widest)} pts)")


if __name__ == "__main__":
    main()
