"""Atos Contract Helper Agent — Streamlit demo app."""
import os
import uuid
import json
import subprocess
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from utils.document_parser import extract_text_from_uploaded_file, detect_contract_type
from utils.claude_client import analyze_contract, compare_contracts
from utils.database import (initialize_schema, clean_duplicate_analyses,
                            save_contract, save_analysis, query,
                            contract_exists, log_audit_event)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Atos Contract Helper Agent",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Login gate ────────────────────────────────────────────────────────────────
def check_password() -> bool:
    if st.session_state.get("authenticated"):
        return True
    st.markdown("## ⚖️ Atos Contract Helper Agent")
    st.markdown("Please log in to continue.")
    with st.form("login_form"):
        pwd = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")
        if submitted:
            app_password = os.getenv("APP_PASSWORD", "")
            if app_password and pwd == app_password:
                st.session_state.authenticated = True
                st.rerun()
            elif not app_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    return False

if not check_password():
    st.stop()

# ── Startup ───────────────────────────────────────────────────────────────────
initialize_schema()
clean_duplicate_analyses()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚖️ Atos")
    st.title("Contract Helper Agent")
    st.caption("AI-powered legal document analysis")
    st.divider()
    page = st.radio(
        "Navigation",
        ["Analyze Contract", "Compare Contracts", "Contract Analytics", "About"],
        index=0,
    )
    st.divider()
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key or api_key == "your_api_key_here":
        st.warning("No API key detected.\nAdd `ANTHROPIC_API_KEY` to your `.env` file.")
    else:
        st.success("Claude API connected")


# ── Helper: risk color ────────────────────────────────────────────────────────
def risk_color(score: int) -> str:
    if score >= 70:
        return "🔴"
    if score >= 40:
        return "🟡"
    return "🟢"


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def run_dbt():
    """Run dbt models against the DuckDB database."""
    dbt_exe = os.path.join(PROJECT_ROOT, ".venv", "Scripts", "dbt")
    result = subprocess.run(
        [dbt_exe, "run", "--project-dir", "dbt_project", "--profiles-dir", "dbt_project"],
        capture_output=True, text=True, cwd=PROJECT_ROOT
    )
    return result.returncode == 0, result.stdout + result.stderr


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Analyze Contract
# ══════════════════════════════════════════════════════════════════════════════
if page == "Analyze Contract":
    st.title("⚖️ Analyze a Contract")
    st.caption("Upload a Word document (.docx) to extract key fields, identify risks, and generate a Legal summary.")

    st.warning(
        "**Confidentiality Notice:** The content of uploaded documents is sent to "
        "Anthropic's Claude API for analysis. Do not upload documents classified above "
        "**INTERNAL**. All uploads are logged for audit purposes."
    )

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload contract (.docx)", type=["docx"])
    with col2:
        contract_type_override = st.selectbox(
            "Contract type (auto-detected if left on Auto)",
            ["Auto-detect", "NDA", "SOW", "HIRING"],
        )
    with col3:
        contract_status = st.selectbox(
            "Status",
            ["Under Review", "Draft", "Executed", "Expired", "Terminated"],
        )

    if uploaded_file:
        with st.spinner("Parsing document..."):
            text = extract_text_from_uploaded_file(uploaded_file)
            detected_type = detect_contract_type(text)
            contract_type = detected_type if contract_type_override == "Auto-detect" else contract_type_override

        st.info(f"Detected contract type: **{contract_type}**  |  Characters: **{len(text):,}**")

        contract_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, uploaded_file.name + text[:200]))
        already_exists = contract_exists(contract_id)
        if already_exists:
            st.warning(
                f"⚠️ **{uploaded_file.name}** has already been analyzed and saved. "
                "Re-analyzing will overwrite the previous result."
            )
            reanalyze = st.checkbox("Yes, re-analyze and overwrite the existing entry")
        else:
            reanalyze = True

        if st.button("Analyze Contract", type="primary", use_container_width=True) and reanalyze:
            if not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "your_api_key_here":
                st.error("Please add your ANTHROPIC_API_KEY to the .env file before analyzing.")
            else:
                with st.spinner("Claude is analyzing your contract..."):
                    try:
                        analysis = analyze_contract(text, contract_type)
                        save_contract(contract_id, uploaded_file.name, contract_type, text, len(text), status=contract_status)
                        save_analysis(contract_id, analysis)
                        log_audit_event(
                            action="analyze",
                            filename=uploaded_file.name,
                            contract_type=contract_type,
                            details=f"risk_score={analysis.get('risk_score', 0)}, contract_id={contract_id}",
                        )

                        # Run dbt in background
                        with st.spinner("Refreshing analytics models..."):
                            run_dbt()

                    except json.JSONDecodeError:
                        st.error("Claude returned an unexpected response. Please try again.")
                        st.stop()
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
                        st.stop()

                # ── Results ──────────────────────────────────────────────────
                st.divider()

                # Risk score banner
                score = analysis.get("risk_score", 0)
                icon = risk_color(score)
                st.metric(f"{icon} Overall Risk Score", f"{score} / 100")

                # Summary
                st.subheader("Legal Summary")
                st.info(analysis.get("summary", "No summary available."))

                # Key fields
                st.subheader("Key Contract Fields")
                fields = {
                    "Party A": analysis.get("party_a", "—"),
                    "Party B": analysis.get("party_b", "—"),
                    "Effective Date": analysis.get("effective_date", "—"),
                    "Expiration Date": analysis.get("expiration_date", "—"),
                    "Governing Law": analysis.get("governing_law", "—"),
                    "Contract Value": analysis.get("contract_value", "—"),
                }
                col_a, col_b = st.columns(2)
                for i, (k, v) in enumerate(fields.items()):
                    (col_a if i % 2 == 0 else col_b).metric(k, v)

                # Risk flags
                risk_flags = analysis.get("risk_flags", [])
                if risk_flags:
                    st.subheader("🚩 Risk Flags")
                    for flag in risk_flags:
                        st.error(f"• {flag}")

                # Missing clauses
                missing = analysis.get("missing_clauses", [])
                if missing:
                    st.subheader("❌ Missing Clauses")
                    for clause in missing:
                        st.warning(f"• {clause}")

                # Key obligations
                obligations = analysis.get("key_obligations", [])
                if obligations:
                    st.subheader("📋 Key Obligations")
                    for ob in obligations:
                        st.markdown(f"• {ob}")

                # Suggested additions
                suggestions = analysis.get("suggested_additions", [])
                if suggestions:
                    st.subheader("💡 Suggested Additions / Corrections")
                    for s in suggestions:
                        st.success(f"• {s}")

                # Clause detail table
                clauses = analysis.get("clauses", [])
                if clauses:
                    st.subheader("📄 Clause Coverage")
                    df_clauses = pd.DataFrame(clauses)
                    df_clauses["present"] = df_clauses["present"].map({True: "✅", False: "❌"})
                    df_clauses["risk_level"] = df_clauses["risk_level"].map(
                        {"high": "🔴 HIGH", "medium": "🟡 MEDIUM", "low": "🟢 LOW"}
                    ).fillna(df_clauses["risk_level"])
                    st.dataframe(
                        df_clauses[["type", "present", "risk_level"]],
                        use_container_width=True,
                        hide_index=True,
                    )

                st.caption(f"Contract ID: `{contract_id}` — saved to local database.")

                # Download report
                st.divider()
                report_lines = [
                    f"ATOS CONTRACT ANALYSIS REPORT",
                    f"{'=' * 50}",
                    f"File:             {uploaded_file.name}",
                    f"Contract Type:    {contract_type}",
                    f"Status:           {contract_status}",
                    f"Risk Score:       {analysis.get('risk_score', 0)} / 100",
                    f"Analyzed:         {__import__('datetime').datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
                    f"",
                    f"KEY FIELDS",
                    f"{'-' * 50}",
                    f"Party A:          {analysis.get('party_a', '—')}",
                    f"Party B:          {analysis.get('party_b', '—')}",
                    f"Effective Date:   {analysis.get('effective_date', '—')}",
                    f"Expiration Date:  {analysis.get('expiration_date', '—')}",
                    f"Governing Law:    {analysis.get('governing_law', '—')}",
                    f"Contract Value:   {analysis.get('contract_value', '—')}",
                    f"",
                    f"SUMMARY",
                    f"{'-' * 50}",
                    analysis.get('summary', '—'),
                    f"",
                    f"RISK FLAGS",
                    f"{'-' * 50}",
                ] + [f"  • {f}" for f in analysis.get('risk_flags', [])] + [
                    f"",
                    f"MISSING CLAUSES",
                    f"{'-' * 50}",
                ] + [f"  • {c}" for c in analysis.get('missing_clauses', [])] + [
                    f"",
                    f"SUGGESTED ADDITIONS",
                    f"{'-' * 50}",
                ] + [f"  • {s}" for s in analysis.get('suggested_additions', [])] + [
                    f"",
                    f"KEY OBLIGATIONS",
                    f"{'-' * 50}",
                ] + [f"  • {o}" for o in analysis.get('key_obligations', [])]
                report_text = "\n".join(report_lines)
                st.download_button(
                    label="⬇️ Download Analysis Report",
                    data=report_text,
                    file_name=f"analysis_{uploaded_file.name.replace('.docx', '')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Compare Contracts
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Compare Contracts":
    st.title("🔀 Compare Two Contracts")
    st.caption("Upload two contracts of the same type to see how they differ.")

    st.warning(
        "**Confidentiality Notice:** Both documents are sent to Anthropic's Claude API "
        "for comparison. Do not upload documents classified above **INTERNAL**. "
        "All comparisons are logged for audit purposes."
    )

    col1, col2 = st.columns(2)
    with col1:
        file_a = st.file_uploader("Contract A", type=["docx"], key="file_a")
    with col2:
        file_b = st.file_uploader("Contract B", type=["docx"], key="file_b")

    contract_type = st.selectbox("Contract type", ["NDA", "SOW", "HIRING"])

    if file_a and file_b:
        if st.button("Compare", type="primary", use_container_width=True):
            if not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "your_api_key_here":
                st.error("Please add your ANTHROPIC_API_KEY to the .env file.")
            else:
                with st.spinner("Comparing contracts..."):
                    text_a = extract_text_from_uploaded_file(file_a)
                    text_b = extract_text_from_uploaded_file(file_b)
                    try:
                        result = compare_contracts(text_a, text_b, contract_type)
                        log_audit_event(
                            action="compare",
                            filename=f"{file_a.name} vs {file_b.name}",
                            contract_type=contract_type,
                            details=f"differences={len(result.get('key_differences', []))}",
                        )
                    except Exception as e:
                        st.error(f"Comparison failed: {e}")
                        st.stop()

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(f"Only in {file_a.name}")
                    for item in result.get("missing_in_b", []):
                        st.markdown(f"• {item}")
                with col2:
                    st.subheader(f"Only in {file_b.name}")
                    for item in result.get("missing_in_a", []):
                        st.markdown(f"• {item}")

                st.subheader("Key Differences")
                for diff in result.get("key_differences", []):
                    st.markdown(f"• {diff}")

                st.subheader("Recommendation")
                st.info(result.get("recommendation", "—"))


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Contract Analytics
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Contract Analytics":
    st.title("📊 Contract Analytics")
    st.caption("Live insights from your contract library, powered by dbt + DuckDB.")

    col_refresh, _ = st.columns([1, 3])
    with col_refresh:
        if st.button("🔄 Refresh dbt Models"):
            with st.spinner("Running dbt..."):
                success, logs = run_dbt()
            if success:
                st.success("dbt models refreshed.")
            else:
                st.error("dbt run failed.")
                with st.expander("dbt logs"):
                    st.code(logs)

    try:
        risks = query("SELECT * FROM mart_contract_risks ORDER BY risk_score DESC")
        expiring = query("SELECT * FROM mart_expiring_soon WHERE expiring_within_90_days = true")
        counterparties = query("SELECT * FROM mart_counterparties")
        coverage = query("SELECT * FROM mart_clause_coverage")
        compliance = query("SELECT * FROM mart_compliance_check ORDER BY compliance_pct ASC")
    except Exception:
        st.info("No data yet — analyze some contracts first, then refresh dbt models.")
        st.stop()

    if risks.empty:
        st.info("No contracts analyzed yet. Head to **Analyze Contract** to get started.")
        st.stop()

    # KPIs
    st.subheader("Overview")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Contracts", len(risks))
    k2.metric("🔴 High Risk", len(risks[risks["risk_tier"] == "HIGH"]))
    k3.metric("⏰ Expiring Soon", len(expiring))
    k4.metric("Counterparties", len(counterparties))

    # Risk distribution
    st.subheader("Risk Distribution")
    import plotly.express as px
    tier_counts = risks["risk_tier"].value_counts().reset_index()
    tier_counts.columns = ["Risk Tier", "Count"]
    color_map = {"HIGH": "#e74c3c", "MEDIUM": "#f39c12", "LOW": "#2ecc71"}
    fig = px.pie(tier_counts, values="Count", names="Risk Tier",
                 color="Risk Tier", color_discrete_map=color_map)
    st.plotly_chart(fig, use_container_width=True)

    # Contract table
    st.subheader("All Contracts")
    display_cols = ["filename", "contract_type", "party_a", "party_b",
                    "effective_date", "expiration_date", "risk_score", "risk_tier", "source_url"]
    available = [c for c in display_cols if c in risks.columns]
    st.dataframe(risks[available], use_container_width=True, hide_index=True)

    # Compliance check
    if not compliance.empty:
        st.subheader("✅ Atos Standards Compliance")
        for _, row in compliance.iterrows():
            status_icon = {"COMPLIANT": "🟢", "NEEDS REVIEW": "🟡", "NON-COMPLIANT": "🔴"}.get(row.get("compliance_status", ""), "⚪")
            st.markdown(
                f"{status_icon} **{row['filename']}** — "
                f"{row['compliance_pct']}% compliant ({row['clauses_present']}/{row['total_required_clauses']} clauses) "
                f"· {row.get('missing_high_risk', 0)} high-risk missing"
            )

    # Expiring soon
    if not expiring.empty:
        st.subheader("⏰ Contracts Expiring Within 90 Days")
        st.dataframe(expiring, use_container_width=True, hide_index=True)

    # Clause coverage
    if not coverage.empty:
        st.subheader("Clause Coverage by Contract Type")
        fig2 = px.bar(
            coverage, x="clause_type", y="coverage_pct",
            color="contract_type", barmode="group",
            labels={"coverage_pct": "Coverage %", "clause_type": "Clause"},
        )
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)

    # Counterparties
    if not counterparties.empty:
        st.subheader("Top Counterparties")
        st.dataframe(counterparties.head(20), use_container_width=True, hide_index=True)

    # Audit log
    st.subheader("🔒 Audit Log")
    try:
        audit = query("SELECT action, filename, contract_type, performed_at, details FROM raw_audit_log ORDER BY performed_at DESC LIMIT 50")
        if not audit.empty:
            st.dataframe(audit, use_container_width=True, hide_index=True)
        else:
            st.info("No audit events recorded yet.")
    except Exception:
        st.info("Audit log not available — refresh dbt models after analyzing a contract.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: About
# ══════════════════════════════════════════════════════════════════════════════
elif page == "About":
    st.title("About Contract Helper Agent")
    st.markdown("""
## What is this?

The **Atos Contract Helper Agent** is an AI-powered tool that helps the Legal team
and anyone at Atos who produces contract-like documents to:

- **Extract** key fields and clauses automatically
- **Flag** risks and missing standard clauses
- **Compare** two contracts side by side
- **Summarize** contracts for Legal review
- **Track** the full contract library over time with analytics

## How it works

```
Upload (.docx) → Claude API → Structured Analysis → DuckDB → dbt Models → Analytics
```

1. You upload a Word document
2. The document is parsed and sent to **Claude** (Anthropic) with a skill-specific prompt
3. Claude returns a structured JSON analysis
4. The analysis is stored in a local **DuckDB** database
5. **dbt** transforms the raw data into analytical models (risk scores, expiry tracking, etc.)
6. The analytics dashboard shows live insights from the growing contract library

## Skill definitions

Each contract type has a `SKILL.md` file that teaches Claude what to look for:

| Skill | File |
|-------|------|
| NDA   | `skills/nda/SKILL.md` |
| SOW   | `skills/sow/SKILL.md` |
| Hiring | `skills/hiring/SKILL.md` |

These files define required clauses, risk flags, and Atos-specific standards.
Edit them to fine-tune the analysis for your organization.

## Tech stack

| Component | Technology |
|-----------|-----------|
| UI | Streamlit |
| AI | Claude claude-sonnet-4-6 (Anthropic) |
| Document parsing | python-docx |
| Database | DuckDB |
| Data transformation | dbt-core + dbt-duckdb |
| Visualization | Plotly |

## Getting started

1. Copy `.env.example` to `.env` and add your `ANTHROPIC_API_KEY`
2. Install dependencies: `pip install -r requirements.txt`
3. Generate sample contracts: `python sample_contracts/generate_samples.py`
4. Run the app: `streamlit run app.py`
""")
