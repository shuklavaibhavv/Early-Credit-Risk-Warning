"""
Credit Risk Quantitative Monitor — Enhanced Interactive Streamlit Dashboard.

Includes:
1. Shaded Risk Bands & Collapse Event Markers for all 7 Group A companies.
2. Peer Overlay comparison (e.g. Credit Suisse vs JPMorgan, Venator vs Air Products).
3. Expandable Quarterly Signal Breakdown (Solvency, Leverage, Coverage, Liquidity, Cash Burn, Merton DD).
4. Early Warning Lead Time Callout Annotations.
"""

import csv
import json
from pathlib import Path
import streamlit as st

# Page metadata
st.set_page_config(
    page_title="Credit Risk Quantitative Monitor",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Dark Navy & Charcoal Styling
CUSTOM_CSS = """
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    #MainMenu, footer, header, .stDeployButton {visibility: hidden; display:none;}

    .kpi-card {
        background-color: #161e2e;
        border: 1px solid #243044;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 6px;
    }
    
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f8fafc;
    }

    .kpi-sub {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 4px;
    }

    .badge-safe { color: #10b981; background-color: rgba(16, 185, 129, 0.15); padding: 4px 8px; border-radius: 4px; font-weight: 600; }
    .badge-warning { color: #f59e0b; background-color: rgba(245, 158, 11, 0.15); padding: 4px 8px; border-radius: 4px; font-weight: 600; }
    .badge-danger { color: #ef4444; background-color: rgba(239, 68, 68, 0.15); padding: 4px 8px; border-radius: 4px; font-weight: 600; }

    .callout-box {
        background-color: rgba(59, 130, 246, 0.12);
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 16px;
        font-size: 0.9rem;
        color: #e2e8f0;
    }

    .header-bar {
        border-bottom: 1px solid #243044;
        padding-bottom: 12px;
        margin-bottom: 24px;
    }

    .header-title { font-size: 1.5rem; font-weight: 700; color: #f8fafc; }
    .header-subtitle { font-size: 0.875rem; color: #94a3b8; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_data
def load_data():
    base_dir = Path(__file__).parent.parent / "data"

    scores_path = base_dir / "composite_credit_scores.csv"
    dtd_path = base_dir / "merton_dtd_signals.csv"
    backtest_path = base_dir / "backtest_summary.json"

    score_rows = []
    if scores_path.exists():
        with open(scores_path, mode="r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                r["composite_credit_score"] = float(r["composite_credit_score"])
                r["composite_pd"] = float(r["composite_pd"])
                r["signal_1_solvency"] = float(r["signal_1_solvency"]) if r.get("signal_1_solvency") not in [None, "", "None"] else None
                r["signal_2_leverage"] = float(r["signal_2_leverage"]) if r.get("signal_2_leverage") not in [None, "", "None"] else None
                r["signal_3_coverage"] = float(r["signal_3_coverage"]) if r.get("signal_3_coverage") not in [None, "", "None"] else None
                r["signal_4_liquidity"] = float(r["signal_4_liquidity"]) if r.get("signal_4_liquidity") not in [None, "", "None"] else None
                r["signal_5_cashflow"] = float(r["signal_5_cashflow"]) if r.get("signal_5_cashflow") not in [None, "", "None"] else None
                r["distance_to_default"] = float(r["distance_to_default"]) if r.get("distance_to_default") not in [None, "", "None"] else None
                score_rows.append(r)

    backtest_summary = {}
    if backtest_path.exists():
        with open(backtest_path, mode="r", encoding="utf-8") as f:
            backtest_summary = json.load(f)

    return score_rows, backtest_summary


# Complete Collapse / Rescue Events for ALL 7 Group A Companies
COLLAPSE_EVENTS = {
    "CS": ("2023Q1", "March 2023: UBS Emergency Rescue"),
    "SIVB": ("2023Q1", "March 2023: FDIC Receivership"),
    "BBBY": ("2023Q2", "April 2023: Chapter 11 Bankruptcy"),
    "PRTY": ("2023Q1", "Jan 2023: Chapter 11 Bankruptcy"),
    "VNTR": ("2023Q2", "May 2023: Chapter 11 Bankruptcy"),
    "RAD": ("2023Q4", "Oct 2023: Chapter 11 Bankruptcy"),
    "WE": ("2023Q4", "Nov 2023: Chapter 11 Bankruptcy"),
}

# Default Benchmark Pairs for Group A Companies
DEFAULT_PAIRS = {
    "CS": "JPM",
    "SIVB": "GS",
    "VNTR": "APD",
    "BBBY": "TGT",
    "PRTY": "COST",
    "RAD": "COST",
    "WE": "MSFT",
}

# Early Warning Callouts (Merton DD Lead Time vs Accounting Deterioration)
EARLY_WARNING_CALLOUTS = {
    "CS": "⚡ <b>Merton DD Early Warning</b>: Market Distance-to-Default flagged severe distress in <b>2022Q2</b> (DD = 1.74, Implied PD = 4.12%), <b>3 quarters before</b> the March 2023 UBS emergency acquisition!",
    "SIVB": "⚡ <b>Merton DD Early Warning</b>: Merton DD dropped to 1.55 in <b>2022Q4</b>, <b>1 quarter before</b> the FDIC receivership in March 2023.",
    "VNTR": "⚡ <b>Merton DD Early Warning</b>: Z-Score and Merton DD entered distress in <b>2022Q1</b> (DD = 1.18), giving <b>5 quarters of advance warning</b> prior to May 2023 bankruptcy.",
    "BBBY": "⚡ <b>Early Warning</b>: Composite risk score crossed 80% threshold in <b>2022Q1</b>, giving <b>5 quarters of advance warning</b> prior to April 2023 bankruptcy.",
    "WE": "⚡ <b>Early Warning</b>: Composite risk score exceeded 80% in <b>2022Q1</b>, providing <b>7 quarters of advance warning</b> prior to Nov 2023 filing.",
}


def main():
    score_rows, backtest_summary = load_data()

    if not score_rows:
        st.error("Data files not found. Please run the model scripts in src/ first.")
        return

    # Header Bar
    st.markdown(
        """
        <div class="header-bar">
            <div class="header-title">CREDIT RISK QUANTITATIVE MONITOR</div>
            <div class="header-subtitle">Multi-Factor Solvency, Merton Distance-to-Default (DD), & Structural Backtesting Dashboard</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar Navigation & Controls
    st.sidebar.title("Navigation")
    view_mode = st.sidebar.radio(
        "Select View",
        [
            "Single Company Deep-Dive",
            "Cohort Risk Heatmap & Ranking",
            "Backtest & Model Performance",
        ],
    )

    tickers = sorted(list(set(r["ticker"] for r in score_rows)))

    if view_mode == "Single Company Deep-Dive":
        st.sidebar.subheader("Company Selection")
        selected_ticker = st.sidebar.selectbox("Primary Company", tickers, index=tickers.index("CS") if "CS" in tickers else 0)

        # Benchmark Overlay Selection
        default_overlay = DEFAULT_PAIRS.get(selected_ticker, "None")
        overlay_options = ["None"] + [t for t in tickers if t != selected_ticker]
        overlay_index = overlay_options.index(default_overlay) if default_overlay in overlay_options else 0
        
        enable_overlay = st.sidebar.checkbox("Overlay Peer Benchmark", value=(default_overlay != "None"))
        overlay_ticker = st.sidebar.selectbox("Peer Benchmark Ticker", overlay_options, index=overlay_index, disabled=not enable_overlay)

        # Primary company data
        primary_rows = [r for r in score_rows if r["ticker"] == selected_ticker]
        primary_rows.sort(key=lambda x: x["quarter"])

        latest_row = primary_rows[-1]
        sector = latest_row["sector"].capitalize()
        group = latest_row["group"]
        is_distressed = group == "A"

        latest_score = latest_row["composite_credit_score"]
        peak_score = max(r["composite_credit_score"] for r in primary_rows)
        latest_dd = latest_row["distance_to_default"]

        # Risk Badge Class
        if latest_score >= 70.0:
            badge_cls = "badge-danger"
            risk_label = "HIGH DISTRESS"
        elif latest_score >= 40.0:
            badge_cls = "badge-warning"
            risk_label = "MODERATE RISK"
        else:
            badge_cls = "badge-safe"
            risk_label = "SAFE / SOLVENT"

        # Top KPI Row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Current Risk Score</div>
                    <div class="kpi-value">{latest_score:.1f}%</div>
                    <div class="kpi-sub"><span class="{badge_cls}">{risk_label}</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Peak Risk Score</div>
                    <div class="kpi-value">{peak_score:.1f}%</div>
                    <div class="kpi-sub">Highest quarterly rating</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            grp_str = "Group A (Distressed Target)" if is_distressed else "Group B (Healthy Control)"
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Sector & Classification</div>
                    <div class="kpi-value" style="font-size: 1.2rem;">{sector}</div>
                    <div class="kpi-sub">{grp_str}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col4:
            dd_str = f"{latest_dd:.2f}" if latest_dd is not None else "Delisted"
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Merton Distance-to-Default</div>
                    <div class="kpi-value">{dd_str}</div>
                    <div class="kpi-sub">Market structural measure</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Early Warning Callout Annotation if available
        if selected_ticker in EARLY_WARNING_CALLOUTS:
            st.markdown(f'<div class="callout-box">{EARLY_WARNING_CALLOUTS[selected_ticker]}</div>', unsafe_allow_html=True)

        # Plotly Trajectory Chart
        st.subheader(f"{selected_ticker} — Composite Credit Risk Trajectory & Peer Comparison")

        try:
            import plotly.graph_objects as go

            quarters = [r["quarter"] for r in primary_rows]
            scores = [r["composite_credit_score"] for r in primary_rows]

            fig = go.Figure()

            # Shaded Threshold Bands
            fig.add_hrect(y0=0, y1=40, fillcolor="rgba(16, 185, 129, 0.10)", line_width=0, annotation_text="Safe Zone (<40%)", annotation_position="top left")
            fig.add_hrect(y0=40, y1=70, fillcolor="rgba(245, 158, 11, 0.12)", line_width=0, annotation_text="Warning Zone (40%-70%)", annotation_position="top left")
            fig.add_hrect(y0=70, y1=100, fillcolor="rgba(239, 68, 68, 0.15)", line_width=0, annotation_text="Distress Zone (>70%)", annotation_position="top left")

            # Primary Line
            fig.add_trace(
                go.Scatter(
                    x=quarters,
                    y=scores,
                    mode="lines+markers",
                    name=f"{selected_ticker} Risk Score (%)",
                    line=dict(color="#ef4444" if is_distressed else "#10b981", width=3.5),
                    marker=dict(size=8),
                    hovertemplate=f"<b>{selected_ticker}</b><br>Quarter: %{{x}}<br>Risk Score: %{{y:.1f}}%<extra></extra>",
                )
            )

            # Benchmark Overlay Line
            if enable_overlay and overlay_ticker != "None":
                overlay_rows = [r for r in score_rows if r["ticker"] == overlay_ticker]
                overlay_rows.sort(key=lambda x: x["quarter"])
                ov_quarters = [r["quarter"] for r in overlay_rows]
                ov_scores = [r["composite_credit_score"] for r in overlay_rows]

                fig.add_trace(
                    go.Scatter(
                        x=ov_quarters,
                        y=ov_scores,
                        mode="lines+markers",
                        name=f"Peer: {overlay_ticker} Risk Score (%)",
                        line=dict(color="#3b82f6", width=2.5, dash="dash"),
                        marker=dict(size=6),
                        hovertemplate=f"<b>{overlay_ticker}</b><br>Quarter: %{{x}}<br>Risk Score: %{{y:.1f}}%<extra></extra>",
                    )
                )

            # Collapse Event Marker (for ALL Group A Companies)
            if selected_ticker in COLLAPSE_EVENTS:
                evt_q, evt_text = COLLAPSE_EVENTS[selected_ticker]
                if evt_q in quarters:
                    evt_idx = quarters.index(evt_q)
                    evt_y = scores[evt_idx]
                    fig.add_trace(
                        go.Scatter(
                            x=[evt_q],
                            y=[evt_y],
                            mode="markers+text",
                            name="Collapse / Rescue Event",
                            marker=dict(color="#dc2626", size=16, symbol="x"),
                            text=[f"  <b>{evt_text}</b>"],
                            textposition="top right",
                            hoverinfo="text",
                        )
                    )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0b0f19",
                plot_bgcolor="#161e2e",
                height=480,
                margin=dict(l=40, r=40, t=40, b=40),
                yaxis=dict(title="Default Risk Score (%)", range=[0, 105], gridcolor="#243044"),
                xaxis=dict(title="Quarter", gridcolor="#243044"),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )

            st.plotly_chart(fig, use_container_width=True)

        except ImportError:
            st.info("Install Plotly for interactive viewing.")

        # Expandable Signal Breakdown Panel
        with st.expander(f"🔍 Detailed Quarterly Signal Breakdown for {selected_ticker}", expanded=True):
            selected_quarter = st.select_slider(
                "Select Quarter for Breakdown",
                options=quarters,
                value=quarters[-1],
            )

            q_row = next(r for r in primary_rows if r["quarter"] == selected_quarter)

            b_col1, b_col2, b_col3, b_col4, b_col5, b_col6 = st.columns(6)

            with b_col1:
                s1_name = "CET1 Ratio" if sector.lower() == "bank" else "Altman Z-Score"
                s1_val = f"{q_row['signal_1_solvency']:.3f}" if q_row["signal_1_solvency"] is not None else "N/A"
                st.metric(s1_name, s1_val)

            with b_col2:
                s2_name = "Loan-to-Deposit" if sector.lower() == "bank" else "Debt / EBITDA"
                s2_val = f"{q_row['signal_2_leverage']:.3f}" if q_row["signal_2_leverage"] is not None else "N/A"
                st.metric(s2_name, s2_val)

            with b_col3:
                s3_name = "NPL Ratio" if sector.lower() == "bank" else "Interest Coverage"
                s3_val = f"{q_row['signal_3_coverage']:.3f}" if q_row["signal_3_coverage"] is not None else "N/A"
                st.metric(s3_name, s3_val)

            with b_col4:
                s4_name = "Net Interest Margin" if sector.lower() == "bank" else "Current Ratio"
                s4_val = f"{q_row['signal_4_liquidity']:.3f}" if q_row["signal_4_liquidity"] is not None else "N/A"
                st.metric(s4_name, s4_val)

            with b_col5:
                s5_name = "Bank Leverage" if sector.lower() == "bank" else "Cash Burn Rate ($M)"
                s5_val = f"{q_row['signal_5_cashflow']:.1f}" if q_row["signal_5_cashflow"] is not None else "N/A"
                st.metric(s5_name, s5_val)

            with b_col6:
                dd_val = f"{q_row['distance_to_default']:.2f}" if q_row["distance_to_default"] is not None else "Delisted"
                st.metric("Merton DD", dd_val)

    elif view_mode == "Cohort Risk Heatmap & Ranking":
        st.subheader("14-Company Cross-Sectional Risk Ranking & Heatmap")

        latest_by_ticker = {}
        for r in score_rows:
            t = r["ticker"]
            if t not in latest_by_ticker or r["quarter"] > latest_by_ticker[t]["quarter"]:
                latest_by_ticker[t] = r

        sorted_comps = sorted(latest_by_ticker.values(), key=lambda x: x["composite_credit_score"], reverse=True)

        try:
            import plotly.express as px

            tickers_list = [r["ticker"] for r in sorted_comps]
            scores_list = [r["composite_credit_score"] for r in sorted_comps]
            groups_list = ["Group A (Distressed)" if r["group"] == "A" else "Group B (Healthy)" for r in sorted_comps]
            sectors_list = [r["sector"].capitalize() for r in sorted_comps]

            color_map = {"Group A (Distressed)": "#ef4444", "Group B (Healthy)": "#10b981"}

            fig = px.bar(
                x=tickers_list,
                y=scores_list,
                color=groups_list,
                color_discrete_map=color_map,
                hover_data={"Sector": sectors_list},
                labels={"x": "Company Ticker", "y": "Composite Risk Score (%)", "color": "Classification"},
                title="Latest Credit Risk Score Ranking Across 14-Company Cohort",
            )

            fig.add_hline(y=60.0, line_dash="dash", line_color="#f59e0b", annotation_text="60% Risk Threshold")

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0b0f19",
                plot_bgcolor="#161e2e",
                height=500,
                xaxis=dict(title="Ticker"),
                yaxis=dict(title="Risk Score (%)", range=[0, 105]),
            )

            st.plotly_chart(fig, use_container_width=True)

        except ImportError:
            st.info("Install Plotly for interactive heatmap.")

        st.subheader("Detailed Cohort Summary Table")
        st.dataframe(
            [
                {
                    "Ticker": r["ticker"],
                    "Group": r["group"],
                    "Sector": r["sector"],
                    "Quarter": r["quarter"],
                    "Risk Score (%)": f"{r['composite_credit_score']:.1f}%",
                    "Solvency Signal": f"{r['signal_1_solvency']:.2f}" if r["signal_1_solvency"] is not None else "N/A",
                    "Leverage Signal": f"{r['signal_2_leverage']:.2f}" if r["signal_2_leverage"] is not None else "N/A",
                    "Merton DD": f"{r['distance_to_default']:.2f}" if r["distance_to_default"] is not None else "Delisted",
                }
                for r in sorted_comps
            ]
        )

    elif view_mode == "Backtest & Model Performance":
        st.subheader("Formal Backtest & Advance Warning Metrics")

        if backtest_summary:
            adv_60 = backtest_summary["group_a_advance_warning"]["threshold_60_pct"]["average_quarters_warning"]
            adv_60_mos = backtest_summary["group_a_advance_warning"]["threshold_60_pct"]["average_months_warning"]
            fp_60_cnt = backtest_summary["group_b_false_positives"]["threshold_60_pct"]["false_positive_count"]
            fp_60_pct = backtest_summary["group_b_false_positives"]["threshold_60_pct"]["false_positive_rate_pct"]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">Average Advance Warning</div>
                        <div class="kpi-value">{adv_60:.2f} Quarters</div>
                        <div class="kpi-sub">~{adv_60_mos:.1f} Months prior to collapse</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">Healthy False Positive Rate</div>
                        <div class="kpi-value">{fp_60_pct:.1f}%</div>
                        <div class="kpi-sub">{fp_60_cnt}/7 Healthy Companies Crossed 60%</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    """
                    <div class="kpi-card">
                        <div class="kpi-title">Model Specification</div>
                        <div class="kpi-value" style="font-size: 1.2rem;">Logistic Regression</div>
                        <div class="kpi-sub">Z-Score + Merton DD + Ratio Engine</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.subheader("Group A Advance Warning Breakdown")
        st.markdown(
            """
            | Company | Ticker | Actual Collapse Quarter | First Threshold Crossing (60%) | Advance Warning (Quarters) | Advance Warning (Months) |
            | :--- | :--- | :--- | :--- | :--- | :--- |
            | **Bed Bath & Beyond** | BBBY | 2023Q2 | 2022Q1 | 5 Quarters | 15.0 Months |
            | **Party City** | PRTY | 2023Q1 | 2022Q1 | 4 Quarters | 12.0 Months |
            | **Rite Aid** | RAD | 2023Q4 | 2022Q1 | 7 Quarters | 21.0 Months |
            | **WeWork** | WE | 2023Q4 | 2022Q1 | 7 Quarters | 21.0 Months |
            | **Credit Suisse** | CS | 2023Q1 | 2022Q2 | 3 Quarters | 9.0 Months |
            | **Silicon Valley Bank** | SIVB | 2023Q1 | 2022Q4 | 1 Quarter | 3.0 Months |
            | **Venator Materials** | VNTR | 2023Q2 | 2022Q1 | 5 Quarters | 15.0 Months |
            """
        )


if __name__ == "__main__":
    main()
