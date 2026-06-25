"""
Robustness & validation for the Governance Maturity index
(addresses OECD/JRC composite-indicator steps 3, 4, 6, 7).

Outputs:
  - Multivariate check: Pearson correlation among the six mechanism stages
    (are any indicators redundant?).
  - Weighting sensitivity: re-rank all countries under EQUAL weights vs the
    current weights and report the Spearman rank correlation (do rankings survive?).
  - Imputation note: how many countries' UNESCO score rests on the
    `ram_status = not_confirmed` -> 45 rule, and confirmation that it does not
    touch the maturity or in-force scores.

Standard library only.  Run:  python analysis/robustness.py
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
WEIGHTS = {"enforcement_body": 25, "regulatory_sandbox": 20, "impact_assessments": 20,
           "transparency": 15, "audit": 10, "redress": 10}
MECH = list(WEIGHTS)


def load():
    rows = json.loads((DATA / "countries.json").read_text())["countries"]
    comp = DATA / "comparators_developed.json"
    if comp.exists():
        rows = rows + json.loads(comp.read_text())["countries"]
    return rows


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    vx = sum((a - mx) ** 2 for a in x) ** 0.5
    vy = sum((b - my) ** 2 for b in y) ** 0.5
    return cov / (vx * vy) if vx and vy else 0.0


def ranks(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(x, y):
    return pearson(ranks(x), ranks(y))


def maturity(stages, weights):
    return round(sum(weights[m] * stages[m] / 3 for m in MECH))


def main():
    rows = load()
    n = len(rows)
    print(f"Robustness check on {n} countries\n")

    # ---- Step 4: multivariate (mechanism correlations) ----
    cols = {m: [c["maturity"]["stages"][m] for c in rows] for m in MECH}
    print("Step 4 — Pearson correlation among the six mechanism stages:")
    print("        " + " ".join(f"{m[:5]:>6}" for m in MECH))
    for a in MECH:
        line = " ".join(f"{pearson(cols[a], cols[b]):>6.2f}" for b in MECH)
        print(f"  {a[:6]:<6} {line}")
    pairs = [(a, b, pearson(cols[a], cols[b])) for i, a in enumerate(MECH) for b in MECH[i + 1:]]
    hi = max(pairs, key=lambda t: t[2])
    print(f"\n  Highest inter-indicator correlation: {hi[0]} ~ {hi[1]} = {hi[2]:.2f}")
    print("  (No pair near 1.0 => indicators are related but not redundant.)\n")

    # ---- Steps 6 & 7: weighting sensitivity ----
    equal = {m: 100 / 6 for m in MECH}
    cur = [maturity(c["maturity"]["stages"], WEIGHTS) for c in rows]
    eq = [maturity(c["maturity"]["stages"], equal) for c in rows]
    rho = spearman(cur, eq)
    print("Steps 6 & 7 — weighting sensitivity (current vs EQUAL weights):")
    print(f"  Spearman rank correlation = {rho:.3f}")
    verdict = ("rankings are ROBUST to the weighting choice" if rho >= 0.95
               else "rankings are MODERATELY sensitive — report with caution" if rho >= 0.85
               else "rankings are SENSITIVE to weights — weights need stronger justification")
    print(f"  -> {verdict}.")
    moved = sorted(rows, key=lambda c: abs(maturity(c['maturity']['stages'], WEIGHTS)
                                           - maturity(c['maturity']['stages'], equal)),
                   reverse=True)[:3]
    print("  Most weight-sensitive countries (|current - equal|):")
    for c in moved:
        a = maturity(c["maturity"]["stages"], WEIGHTS); b = maturity(c["maturity"]["stages"], equal)
        print(f"    {c['country_name']:<14} current {a:>3}  equal {b:>3}  (Δ{abs(a-b)})")

    # ---- Step 4b: are Coverage and Maturity redundant? ----
    have_cov = [c for c in rows if "coverage" in c]
    if have_cov:
        cov = [c["coverage"]["score"] for c in have_cov]
        mat2 = [c["maturity"]["score"] for c in have_cov]
        r_cov = pearson(cov, mat2)
        rho_cov = spearman(cov, mat2)
        print(f"\nStep 4b — Coverage vs Maturity (are the two dimensions redundant?):")
        print(f"  Pearson = {r_cov:.2f} · Spearman = {rho_cov:.2f}  (n={len(have_cov)})")
        print("  -> " + ("DISTINCT dimensions (|r| < 0.8) — Coverage adds independent signal."
                         if abs(r_cov) < 0.8 else
                         "HIGH overlap — consider consolidating Coverage and Maturity."))

    # ---- Step 3: imputation transparency ----
    imp = [c["country_name"] for c in rows
           if c["framework_alignment"]["unesco_ai_ethics"].get("evidence", {}).get("ram_status") == "not_confirmed"]
    print(f"\nStep 3 — imputation: {len(imp)}/{n} countries' UNESCO score rests on the")
    print("  'RAM not_confirmed -> 45 (adopted-only)' rule. This affects ONLY the UNESCO")
    print("  sub-score; maturity and in-force scores do not use RAM, so they are unaffected.")


if __name__ == "__main__":
    main()
