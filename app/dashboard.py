"""
Global South AI Governance Tracker
Interactive dashboard for mapping AI governance adoption across developing economies

Author: Sana Asif Ahmad
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Global South AI Governance Tracker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
    }
    .insight-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    .framework-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.25rem;
    }
    .high { background: #d4edda; color: #155724; }
    .partial { background: #fff3cd; color: #856404; }
    .low { background: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load country and framework data from JSON files"""
    data_dir = Path(__file__).parent.parent / "data"
    
    with open(data_dir / "countries.json", "r") as f:
        countries_data = json.load(f)
    
    with open(data_dir / "frameworks.json", "r") as f:
        frameworks_data = json.load(f)
    
    return countries_data, frameworks_data

# Implementation indicator weights (must match METHODOLOGY.md). The score is
# DERIVED from these booleans so it can never drift out of sync with the data.
IMPL_WEIGHTS = {
    "has_enforcement_body": 25,
    "has_regulatory_sandbox": 20,
    "has_impact_assessments": 20,
    "has_transparency_requirements": 15,
    "has_audit_mechanisms": 10,
    "has_redress_mechanisms": 10,
}


def implementation_score(impl):
    """Deterministic weighted sum of the six in-force indicators."""
    return sum(w for k, w in IMPL_WEIGHTS.items() if impl.get(k))


def process_countries_df(countries_data):
    """Convert countries JSON to DataFrame for analysis"""
    records = []
    for country in countries_data["countries"]:
        record = {
            "country_code": country["country_code"],
            "country_name": country["country_name"],
            "region": country["region"],
            "income_level": country["income_level"],
            "population_millions": country["population_millions"],
            "has_strategy": country["ai_strategy"]["has_national_strategy"],
            "strategy_year": country["ai_strategy"].get("year_published"),
            "eu_ai_act_score": country["framework_alignment"]["eu_ai_act"]["adoption_score"],
            "eu_ai_act_status": country["framework_alignment"]["eu_ai_act"]["adoption_status"],
            "unesco_score": country["framework_alignment"]["unesco_ai_ethics"]["adoption_score"],
            "oecd_score": country["framework_alignment"]["oecd_ai_principles"]["adoption_score"],
            "implementation_score": implementation_score(country["implementation_status"]),
            "maturity_score": country.get("maturity", {}).get("score", 0),
            "maturity_level": country.get("maturity", {}).get("level", "—"),
            "has_enforcement": country["implementation_status"]["has_enforcement_body"],
            "has_sandbox": country["implementation_status"]["has_regulatory_sandbox"],
            "has_impact_assessment": country["implementation_status"]["has_impact_assessments"],
            "uses_eu_categories": country["risk_classification"]["uses_eu_categories"],
            "custom_high_risk": country["risk_classification"]["custom_high_risk"]
        }
        records.append(record)
    
    return pd.DataFrame(records)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Load data
    try:
        countries_data, frameworks_data = load_data()
        df = process_countries_df(countries_data)
    except FileNotFoundError:
        st.error("Data files not found. Please ensure countries.json and frameworks.json are in the data/ directory.")
        st.stop()
    
    # Header
    st.markdown('<p class="main-header">🌍 Global South AI Governance Tracker</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Interactive dashboard mapping AI governance adoption across developing economies</p>', unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    regions = ["All"] + sorted(df["region"].unique().tolist())
    selected_region = st.sidebar.selectbox("Region", regions)
    
    income_levels = ["All"] + sorted(df["income_level"].unique().tolist())
    selected_income = st.sidebar.selectbox("Income Level", income_levels)
    
    framework_focus = st.sidebar.selectbox(
        "Framework Focus",
        ["EU AI Act", "UNESCO AI Ethics", "OECD AI Principles"]
    )
    
    # Apply filters
    filtered_df = df.copy()
    if selected_region != "All":
        filtered_df = filtered_df[filtered_df["region"] == selected_region]
    if selected_income != "All":
        filtered_df = filtered_df[filtered_df["income_level"] == selected_income]
    
    # ========================================================================
    # KEY METRICS ROW
    # ========================================================================
    
    with st.expander("ℹ️ How to read this dashboard — why the EU AI Act is the baseline & how the 'gap' is measured"):
        st.markdown(
            """
**Why the EU AI Act is the baseline.** It is the only *comprehensive, binding* AI
law currently in force — UNESCO, OECD, AU and ASEAN instruments are non-binding
principles. Its four risk tiers give clear, comparable checkpoints, and because it
applies to anyone selling AI into the EU market (the "Brussels Effect"), countries
worldwide actually respond to it. We use it as a **common ruler**, *not* a
prescription — a key finding here is exactly where local priorities (agriculture,
mobile money, climate) justify *diverging* from EU categories. Every country is
also scored against UNESCO and OECD so no single framework dominates.

**How the gap is measured.**
- **Adoption Score (0–100):** how closely *written policy* aligns with the EU AI Act — rules on paper.
- **Implementation Score (0–100):** how much is *actually operational* — enforcement body, sandbox, impact assessments, transparency, audit, and redress mechanisms (weighted).
- **Adoption–Implementation Gap = Adoption − Implementation.** A large gap = ambitious policy that isn't yet enforceable ("policy ahead of practice"); a small gap = policy and capacity in step.

*Factual fields (internet access, data-protection laws, OECD/GPAI membership) are
sourced (World Bank, OECD). Alignment and implementation **scores are analyst
estimates** — see METHODOLOGY.md.*
            """
        )

    st.markdown("### 📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Countries Tracked",
            value=len(filtered_df),
            delta=f"{len(df)} total" if len(filtered_df) < len(df) else None
        )
    
    with col2:
        avg_adoption = filtered_df["eu_ai_act_score"].mean()
        st.metric(
            label="Avg EU AI Act Adoption",
            value=f"{avg_adoption:.0f}%",
            delta=f"{avg_adoption - df['eu_ai_act_score'].mean():+.0f}% vs all" if selected_region != "All" else None
        )
    
    with col3:
        avg_impl = filtered_df["implementation_score"].mean()
        st.metric(
            label="Avg Implementation Score",
            value=f"{avg_impl:.0f}%",
            help="Measures actual enforcement mechanisms, not just policy adoption"
        )
    
    with col4:
        gap = avg_adoption - avg_impl
        st.metric(
            label="Adoption-Implementation Gap",
            value=f"{gap:.0f} pts",
            delta="Higher = more policy, less action",
            delta_color="inverse"
        )
    
    # ========================================================================
    # MAIN VISUALIZATIONS
    # ========================================================================
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Regional Overview", 
        "📈 Framework Adoption", 
        "🔍 Implementation Gap",
        "⚠️ Risk Categories"
    ])
    
    # Tab 1: Regional Overview Map
    with tab1:
        st.markdown("### Regional AI Governance Landscape")
        
        # Create choropleth map
        fig_map = px.choropleth(
            filtered_df,
            locations="country_code",
            color="eu_ai_act_score",
            hover_name="country_name",
            hover_data={
                "country_code": False,
                "eu_ai_act_score": ":.0f",
                "implementation_score": ":.0f",
                "region": True
            },
            color_continuous_scale="RdYlGn",
            range_color=[0, 100],
            labels={
                "eu_ai_act_score": "EU AI Act Adoption (%)",
                "implementation_score": "Implementation (%)"
            }
        )
        
        fig_map.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth'
            ),
            margin=dict(l=0, r=0, t=30, b=0),
            height=500
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Regional summary table
        st.markdown("#### Regional Summary")
        regional_summary = filtered_df.groupby("region").agg({
            "country_name": "count",
            "eu_ai_act_score": "mean",
            "unesco_score": "mean",
            "implementation_score": "mean",
            "has_enforcement": "sum"
        }).round(1)
        
        regional_summary.columns = [
            "Countries", "EU AI Act Avg", "UNESCO Avg", 
            "Implementation Avg", "With Enforcement Body"
        ]
        
        st.dataframe(regional_summary, use_container_width=True)
    
    # Tab 2: Framework Adoption Comparison
    with tab2:
        st.markdown("### Framework Adoption by Country")
        
        # Framework comparison bar chart
        framework_cols = {
            "EU AI Act": "eu_ai_act_score",
            "UNESCO AI Ethics": "unesco_score", 
            "OECD AI Principles": "oecd_score"
        }
        
        selected_col = framework_cols[framework_focus]
        
        fig_bar = px.bar(
            filtered_df.sort_values(selected_col, ascending=True),
            x=selected_col,
            y="country_name",
            orientation="h",
            color=selected_col,
            color_continuous_scale="RdYlGn",
            range_color=[0, 100],
            labels={selected_col: f"{framework_focus} Adoption Score"}
        )
        
        fig_bar.update_layout(
            height=max(400, len(filtered_df) * 50),
            yaxis_title="",
            xaxis_title="Adoption Score (%)",
            showlegend=False
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Framework comparison scatter
        st.markdown("#### Multi-Framework Comparison")
        
        fig_scatter = px.scatter(
            filtered_df,
            x="eu_ai_act_score",
            y="unesco_score",
            size="population_millions",
            color="region",
            hover_name="country_name",
            labels={
                "eu_ai_act_score": "EU AI Act Adoption (%)",
                "unesco_score": "UNESCO AI Ethics Adoption (%)",
                "population_millions": "Population (M)"
            }
        )
        
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Tab 3: Implementation Gap Analysis
    with tab3:
        st.markdown("### The Adoption-Implementation Gap")
        
        st.markdown("""
        <div class="insight-box">
        <strong>Key Finding:</strong> Most countries score significantly higher on framework adoption than actual implementation. 
        This "paper compliance" gap is a critical indicator of where governance exists on paper but not in practice.
        </div>
        """, unsafe_allow_html=True)
        
        # Gap analysis chart
        gap_df = filtered_df.copy()
        gap_df["gap"] = gap_df["eu_ai_act_score"] - gap_df["implementation_score"]
        gap_df = gap_df.sort_values("gap", ascending=False)
        
        fig_gap = go.Figure()
        
        fig_gap.add_trace(go.Bar(
            name="EU AI Act Adoption",
            x=gap_df["country_name"],
            y=gap_df["eu_ai_act_score"],
            marker_color="#4CAF50"
        ))
        
        fig_gap.add_trace(go.Bar(
            name="Governance Maturity",
            x=gap_df["country_name"],
            y=gap_df["maturity_score"],
            marker_color="#2196F3"
        ))

        fig_gap.add_trace(go.Bar(
            name="Implementation (in force)",
            x=gap_df["country_name"],
            y=gap_df["implementation_score"],
            marker_color="#FF9800"
        ))

        fig_gap.update_layout(
            barmode="group",
            xaxis_tickangle=-45,
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            yaxis_title="Score (%)"
        )
        
        st.plotly_chart(fig_gap, use_container_width=True)
        
        # Implementation components breakdown
        st.markdown("#### Implementation Components")
        
        impl_cols = ["has_enforcement", "has_sandbox", "has_impact_assessment"]
        impl_labels = ["Enforcement Body", "Regulatory Sandbox", "Impact Assessments"]
        
        impl_summary = []
        for col, label in zip(impl_cols, impl_labels):
            count = filtered_df[col].sum()
            pct = count / len(filtered_df) * 100
            impl_summary.append({"Component": label, "Countries": count, "Percentage": pct})
        
        impl_df = pd.DataFrame(impl_summary)
        
        fig_impl = px.bar(
            impl_df,
            x="Component",
            y="Percentage",
            text="Countries",
            color="Percentage",
            color_continuous_scale="RdYlGn"
        )
        
        fig_impl.update_traces(texttemplate="%{text} countries", textposition="outside")
        fig_impl.update_layout(height=400, showlegend=False)
        
        st.plotly_chart(fig_impl, use_container_width=True)
    
    # Tab 4: Risk Categories
    with tab4:
        st.markdown("### Risk Category Divergence")
        
        st.markdown("""
        <div class="insight-box">
        <strong>Key Finding:</strong> Developing economies often classify different AI systems as "high-risk" 
        compared to the EU framework. This reflects local economic priorities and risk perceptions.
        </div>
        """, unsafe_allow_html=True)
        
        # Count custom high-risk categories
        all_categories = []
        for _, row in filtered_df.iterrows():
            for cat in row["custom_high_risk"]:
                all_categories.append({
                    "country": row["country_name"],
                    "category": cat,
                    "uses_eu": row["uses_eu_categories"]
                })
        
        cat_df = pd.DataFrame(all_categories)
        cat_counts = cat_df["category"].value_counts().head(15)
        
        fig_cat = px.bar(
            x=cat_counts.values,
            y=cat_counts.index,
            orientation="h",
            labels={"x": "Number of Countries", "y": "High-Risk Category"},
            color=cat_counts.values,
            color_continuous_scale="Reds"
        )
        
        fig_cat.update_layout(
            height=500,
            showlegend=False,
            yaxis=dict(autorange="reversed")
        )
        
        st.plotly_chart(fig_cat, use_container_width=True)
        
        # Categories NOT in EU framework
        st.markdown("#### Categories Unique to Global South (Not in EU AI Act High-Risk List)")
        
        eu_high_risk = [
            "biometric identification", "critical infrastructure", "education",
            "employment", "access to essential services", "law enforcement",
            "migration", "administration of justice"
        ]
        
        unique_cats = []
        for cat in cat_counts.index:
            if not any(eu_cat in cat.lower() for eu_cat in eu_high_risk):
                unique_cats.append(cat)
        
        if unique_cats:
            cols = st.columns(3)
            for i, cat in enumerate(unique_cats[:6]):
                with cols[i % 3]:
                    st.markdown(f"• **{cat}**")
    
    # ========================================================================
    # COUNTRY DEEP DIVE
    # ========================================================================
    
    st.markdown("---")
    st.markdown("### 🔎 Country Deep Dive")
    
    selected_country = st.selectbox(
        "Select a country for detailed analysis",
        filtered_df["country_name"].tolist()
    )
    
    if selected_country:
        country_data = next(
            c for c in countries_data["countries"]
            if c["country_name"] == selected_country
        )
        impl = country_data["implementation_status"]
        coding = impl.get("coding_status", "provisional")
        badge = "✅ evidence-coded" if coding == "evidence_coded" else "🟡 provisional (estimate)"

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"#### {selected_country} &nbsp;·&nbsp; *{badge}*")
            st.markdown(f"**Region:** {country_data['region']}")
            st.markdown(f"**Income Level:** {country_data['income_level'].replace('_', ' ').title()}")
            st.markdown(f"**Population:** {country_data['population_millions']}M")

            if country_data["ai_strategy"]["has_national_strategy"]:
                st.markdown(f"**National AI Strategy:** {country_data['ai_strategy']['strategy_name']} ({country_data['ai_strategy']['year_published']})")
                st.markdown(f"**Lead Agency:** {country_data['ai_strategy']['lead_agency']}")

        with col2:
            st.markdown("#### Framework Alignment")

            frameworks = country_data["framework_alignment"]
            for fw_name, fw_data in frameworks.items():
                score = fw_data["adoption_score"]
                status = fw_data["adoption_status"]

                status_class = "high" if score >= 60 else "partial" if score >= 30 else "low"

                st.markdown(f"""
                <span class="framework-badge {status_class}">
                    {fw_name.replace('_', ' ').upper()}: {score}% ({status})
                </span>
                """, unsafe_allow_html=True)

                st.caption(fw_data["notes"])

                # Evidence basis for the fact-derived frameworks
                ev = fw_data.get("evidence")
                if ev and fw_name == "unesco_ai_ethics":
                    st.caption(f"📋 UNESCO RAM: **{ev.get('ram_status', '—')}** · adopted 2021 Recommendation: "
                               f"{'yes' if ev.get('adopted_2021_recommendation') else 'no'}")
                elif ev and fw_name == "oecd_ai_principles":
                    flags = [("OECD member" if ev.get("oecd_member") else "not OECD member"),
                             ("AI-Principles adherent" if ev.get("ai_principles_adherent") else "not an adherent"),
                             ("GPAI member" if ev.get("gpai_member") else "not GPAI")]
                    st.caption("🏛️ " + " · ".join(flags))

        # Implementation breakdown — is governance actually IN FORCE?
        st.markdown("#### ⚙️ Implementation — is it in force?")
        impl_score = implementation_score(impl)
        eu_score = country_data["framework_alignment"]["eu_ai_act"]["adoption_score"]
        st.markdown(f"**Implementation score: {impl_score}/100** &nbsp;·&nbsp; *{badge}*")

        indicators = [
            ("has_enforcement_body", "Enforcement body"),
            ("has_regulatory_sandbox", "Regulatory sandbox"),
            ("has_impact_assessments", "Impact assessments"),
            ("has_transparency_requirements", "Transparency rules"),
            ("has_audit_mechanisms", "Audit mechanisms"),
            ("has_redress_mechanisms", "Redress mechanisms"),
        ]
        ic1, ic2 = st.columns(2)
        for i, (key, label) in enumerate(indicators):
            mark = "✅" if impl.get(key) else "⬜"
            (ic1 if i % 2 == 0 else ic2).markdown(f"{mark} {label}")

        evidence = impl.get("evidence")
        if evidence:
            with st.expander("📑 Evidence & sources (per indicator)"):
                for key, label in indicators:
                    e = evidence.get(key)
                    if e:
                        st.markdown(
                            f"**{label}:** {'✅ in force' if e['value'] else '❌ not in force'} — "
                            f"{e['evidence']}  \n[source]({e['source']}) · _as of {e.get('as_of', '—')}_"
                        )
        else:
            st.caption("Implementation indicators are provisional estimates — not yet evidence-coded. See docs/coding_worksheet.md.")

        # Governance Maturity — how far along the journey (vs. binary "in force")
        mat = country_data.get("maturity")
        if mat:
            st.markdown(f"#### 🌱 Governance Maturity: {mat['score']}/100 &nbsp;·&nbsp; *{mat['level']}*")
            st.caption(mat.get("basis", ""))
            stage_word = {0: "absent", 1: "committed", 2: "drafted/proposed", 3: "in force"}
            mech_labels = {
                "enforcement_body": "Enforcement body", "regulatory_sandbox": "Regulatory sandbox",
                "impact_assessments": "Impact assessments", "transparency": "Transparency rules",
                "audit": "Audit mechanisms", "redress": "Redress mechanisms",
            }
            mc1, mc2 = st.columns(2)
            for i, (k, label) in enumerate(mech_labels.items()):
                stg = mat["stages"].get(k, 0)
                bar = "🟩" * stg + "⬜" * (3 - stg)
                (mc1 if i % 2 == 0 else mc2).markdown(f"{bar} {label} — *{stage_word[stg]}*")

        st.info(f"**Adoption–Implementation gap:** EU AI Act adoption {eu_score} − implementation {impl_score} "
                f"= **{eu_score - impl_score} points** &nbsp;·&nbsp; Maturity {mat['score'] if mat else '—'}/100")

        # Key developments timeline
        st.markdown("#### Recent Developments")
        for dev in country_data.get("key_developments", [])[-3:]:
            st.markdown(f"• **{dev['date']}**: {dev['event']}")
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p><strong>Global South AI Governance Tracker</strong></p>
        <p>Built by <a href="https://github.com/YOUR_USERNAME">Sana Asif Ahmad</a> | 
        Data from UN Development Coordination Office, national AI strategies, and regulatory filings</p>
        <p>Last updated: May 2026 | <a href="https://github.com/YOUR_USERNAME/ai-governance-tracker">View on GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
