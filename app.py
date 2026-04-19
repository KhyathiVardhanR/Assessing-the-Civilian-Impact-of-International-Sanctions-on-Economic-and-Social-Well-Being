"""
Streamlit App: Assessing the Civilian Impact of International Sanctions
on Economic and Social Well-Being

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sanctions & Civilian Well-Being",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Data Loading ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = "data/processed"
    data = {}

    # Feature-engineered dataset (with country names)
    try:
        data["df"] = pd.read_csv(f"{base}/feature_engineered_dataset.csv")
    except FileNotFoundError:
        data["df"] = pd.DataFrame()

    # Composite well-being index
    try:
        data["wb_index"] = pd.read_csv(f"{base}/wellbeing_index.csv")
    except FileNotFoundError:
        data["wb_index"] = pd.DataFrame()

    # Merged dataset (same but smaller)
    try:
        data["merged"] = pd.read_csv(f"{base}/merged_dataset.csv")
    except FileNotFoundError:
        data["merged"] = pd.DataFrame()

    # Model metrics
    try:
        data["metrics"] = pd.read_csv(f"{base}/model_metrics.csv")
    except FileNotFoundError:
        data["metrics"] = pd.DataFrame()

    # Model comparison
    try:
        data["comparison"] = pd.read_csv(f"{base}/three_model_comparison.csv")
    except FileNotFoundError:
        try:
            data["comparison"] = pd.read_csv(f"{base}/extended_model_comparison.csv")
        except FileNotFoundError:
            data["comparison"] = pd.DataFrame()

    # Permutation importance
    try:
        data["perm_imp"] = pd.read_csv(f"{base}/random_forest_permutation_importance.csv")
    except FileNotFoundError:
        data["perm_imp"] = pd.DataFrame()

    # FE regression results
    try:
        data["fe_results"] = pd.read_csv(f"{base}/fe_regression_results.csv")
    except FileNotFoundError:
        data["fe_results"] = pd.DataFrame()

    # Event study stats
    try:
        data["event_study"] = pd.read_csv(f"{base}/event_study_stats.csv")
    except FileNotFoundError:
        data["event_study"] = pd.DataFrame()

    # Multi-outcome FE results
    try:
        data["multi_outcome"] = pd.read_csv(f"{base}/multi_outcome_fe_results.csv")
    except FileNotFoundError:
        data["multi_outcome"] = pd.DataFrame()

    # Test predictions
    try:
        data["test_preds"] = pd.read_csv(f"{base}/test_predictions.csv")
    except FileNotFoundError:
        data["test_preds"] = pd.DataFrame()

    return data


data = load_data()

# Remove World Bank regional aggregates and income-group codes —
# these are not sovereign countries and should not appear in the analysis
WB_AGGREGATES = {
    'AFE','AFW','ARB','CEB','CSS','EAP','EAR','EAS','ECA','ECS',
    'EMU','EUU','FCS','HIC','HPC','IBD','IBT','IDA','IDB','IDX',
    'LAC','LCN','LDC','LIC','LMC','LMY','LTE','MEA','MIC','MNA',
    'NAC','OED','OSS','PRE','PSS','PST','SAS','SSA','SSF','SST',
    'TEA','TEC','TLA','TMN','TSA','TSS','UMC','WLD'
}
for key in data:
    if isinstance(data[key], pd.DataFrame) and not data[key].empty and 'country_code' in data[key].columns:
        data[key] = data[key][~data[key]['country_code'].isin(WB_AGGREGATES)].copy()

df = data["df"]

# ─── Sidebar Navigation ───────────────────────────────────────────────────────
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a Page",
    ["🏠 Overview", "🔍 Data Explorer", "📊 Sanction Impact", "🤖 Model Results", "📈 Advanced Analysis", "📋 Findings"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Project:** Assessing the Civilian Impact of International Sanctions on Economic and Social Well-Being")
st.sidebar.markdown("**Course:** Introduction to Data Science")
st.sidebar.markdown("**Data:** 1995–2024 Country Panel")

# ─── Helper Functions ─────────────────────────────────────────────────────────
def metric_card(col, label, value, delta=None):
    col.metric(label=label, value=value, delta=delta)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.title("🌍 Assessing the Civilian Impact of International Sanctions")
    st.subheader("on Economic and Social Well-Being")

    st.markdown("""
    This interactive dashboard presents findings from a data science project that investigates
    how **international sanctions** affect the welfare of civilian populations.

    Rather than focusing on whether sanctions achieve their political goals, this project asks:
    **Do sanctions harm ordinary people, and through what economic channels?**
    """)

    # Key metrics
    if not df.empty:
        st.markdown("---")
        st.subheader("Dataset at a Glance")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Countries", df["country_code"].nunique() if "country_code" in df.columns else "—")
        with col2:
            ymin = int(df["year"].min()) if "year" in df.columns else "—"
            ymax = int(df["year"].max()) if "year" in df.columns else "—"
            st.metric("Year Range", f"{ymin}–{ymax}")
        with col3:
            total = f"{len(df):,}"
            st.metric("Observations", total)
        with col4:
            if "sanction_active" in df.columns:
                n_sanctioned = int(df["sanction_active"].sum())
                st.metric("Sanctioned Obs.", f"{n_sanctioned:,}")
        with col5:
            if "sanction_active" in df.columns:
                pct = df["sanction_active"].mean() * 100
                st.metric("% Sanctioned", f"{pct:.1f}%")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Research Framework")
        st.markdown("""
        **Research Question:**
        How do international sanctions affect civilian economic and social well-being
        over time, and through what transmission channels do these effects operate?

        **Transmission Mechanism:**
        ```
        Sanctions
          → Trade restrictions & financial constraints
          → Import/export contraction (food, medicine, energy)
          → Price instability & macroeconomic stress
          → Poverty & household welfare decline
          → Child health & education outcomes
        ```

        **Key Variables:**
        - **Dependent:** Child Mortality U5, School Enrollment, Unemployment
        - **Treatment:** Sanction Active (binary), Sanction Intensity (0–1)
        - **Controls:** GDP Growth, Inflation, Conflict, Regime Score
        """)

    with col_right:
        st.subheader("Methodology")
        st.markdown("""
        This project uses a **country-year panel dataset** and applies:

        | Method | Purpose |
        |--------|---------|
        | Descriptive Analysis | Understand sanction patterns & welfare gaps |
        | Fixed-Effects Regression | Causal inference: within-country effects |
        | Event-Study Analysis | Dynamic effects around sanction onset |
        | Gradient Boosting | Best predictive model (Test R² ≈ 0.54) |
        | Heterogeneous Effects | By sanction type and political regime |
        | Multi-Outcome Analysis | Health, education, and labor outcomes |

        **Four data sources integrated:**
        1. Global Sanctions Data Base (GSDB)
        2. UN Comtrade (trade flows)
        3. World Bank WDI (welfare indicators)
        4. UCDP / Polity V (conflict & regime data)
        """)

    st.markdown("---")
    st.info("Use the sidebar to navigate between pages. Start with **Data Explorer** to understand the dataset, then explore **Sanction Impact**, **Model Results**, and **Advanced Analysis**.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2: DATA EXPLORER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Data Explorer":
    st.title("🔍 Data Explorer")
    st.markdown("Filter and explore the country-year panel dataset.")

    if df.empty:
        st.error("Dataset not found. Please run the notebooks first.")
        st.stop()

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        years = sorted(df["year"].dropna().unique().astype(int))
        year_range = st.slider("Year Range", min_value=years[0], max_value=years[-1],
                               value=(years[0], years[-1]))
    with col2:
        sanction_filter = st.selectbox("Sanction Status", ["All", "Sanctioned Only", "Not Sanctioned"])
    with col3:
        if "country" in df.columns:
            countries = ["All"] + sorted(df["country"].dropna().unique().tolist())
            country_filter = st.selectbox("Country", countries)
        else:
            country_filter = "All"

    # Apply filters
    df_filtered = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])].copy()
    if sanction_filter == "Sanctioned Only":
        df_filtered = df_filtered[df_filtered["sanction_active"] == 1]
    elif sanction_filter == "Not Sanctioned":
        df_filtered = df_filtered[df_filtered["sanction_active"] == 0]
    if country_filter != "All" and "country" in df.columns:
        df_filtered = df_filtered[df_filtered["country"] == country_filter]

    st.markdown(f"**Showing {len(df_filtered):,} observations**")

    # Time series
    outcome_var = st.selectbox(
        "Select outcome variable to visualize:",
        ["child_mortality_u5", "school_enrollment", "unemployment_rate",
         "inflation_rate", "gdp_growth", "poverty_rate"]
    )

    if outcome_var in df_filtered.columns:
        ts_data = df_filtered.groupby(["year", "sanction_active"])[outcome_var].mean().reset_index()
        ts_data["Sanction Status"] = ts_data["sanction_active"].map({0: "Not Sanctioned", 1: "Sanctioned"})

        fig = px.line(
            ts_data, x="year", y=outcome_var,
            color="Sanction Status",
            color_discrete_map={"Not Sanctioned": "#2196F3", "Sanctioned": "#F44336"},
            title=f"Average {outcome_var.replace('_', ' ').title()} Over Time by Sanction Status",
            labels={"year": "Year", outcome_var: outcome_var.replace("_", " ").title()}
        )
        fig.update_layout(height=400, hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    # Data table
    with st.expander("View Raw Data"):
        display_cols = ["country", "year", "sanction_active", "sanction_intensity_index",
                       "child_mortality_u5", "gdp_growth", "inflation_rate",
                       "school_enrollment", "unemployment_rate", "regime_score",
                       "conflict_incidence"]
        display_cols = [c for c in display_cols if c in df_filtered.columns]
        st.dataframe(df_filtered[display_cols].sort_values(["country", "year"] if "country" in display_cols else ["year"]).reset_index(drop=True), height=300)

    # Summary statistics
    st.subheader("Summary Statistics")
    num_cols = [c for c in ["child_mortality_u5", "gdp_growth", "inflation_rate",
                             "school_enrollment", "unemployment_rate",
                             "sanction_intensity_index", "regime_score"] if c in df_filtered.columns]
    if num_cols:
        st.dataframe(df_filtered[num_cols].describe().round(2))


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3: SANCTION IMPACT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Sanction Impact":
    st.title("📊 Sanction Impact on Civilian Well-Being")
    st.markdown("Sanctions harm civilians across **multiple dimensions** — health, education, gender equity, and economic stability.")

    if df.empty:
        st.error("Dataset not found. Please run the notebooks first.")
        st.stop()

    # Tab layout
    tab1, tab2, tab3, tab4 = st.tabs(["All 5 Outcomes", "Composite Index", "Sanction Episodes", "Geographic View"])

    with tab1:
        st.subheader("5 Civilian Well-Being Dimensions: Sanctioned vs Not Sanctioned")
        st.caption("All comparisons are descriptive (unadjusted). See Advanced Analysis for causal fixed-effects estimates.")

        # Define all 5 outcomes with their dimension and direction
        all_outcomes = [
            ("child_mortality_u5",  "Health",          "#e74c3c", "bad",  "Higher = worse"),
            ("school_enrollment",   "Education",       "#2980b9", "good", "Higher = better"),
            ("SE.PRM.NENR.FE",     "Gender Equity",   "#8e44ad", "good", "Girls enrollment — Higher = better"),
            ("unemployment_rate",   "Economic",        "#27ae60", "bad",  "Higher = worse"),
            ("inflation_rate",      "Price Stability", "#e67e22", "bad",  "Higher = worse"),
        ]

        # Build comparison table
        comp_rows = []
        for var, dim, color, direction, note in all_outcomes:
            if var not in df.columns:
                continue
            sub = df.dropna(subset=[var])
            not_s = sub[sub["sanction_active"]==0][var].mean()
            is_s  = sub[sub["sanction_active"]==1][var].mean()
            diff  = is_s - not_s
            # Flag direction: negative diff on 'bad' variable = sanctions worsen it
            worsen = (direction == "bad" and diff > 0) or (direction == "good" and diff < 0)
            comp_rows.append({
                "Dimension": dim,
                "Outcome": var.replace("_"," ").title(),
                "Not Sanctioned": round(not_s, 2),
                "Sanctioned": round(is_s, 2),
                "Difference": round(diff, 2),
                "Sanctions Harm?": "Yes ⚠️" if worsen else "No ✓"
            })
        comp_df = pd.DataFrame(comp_rows)
        st.dataframe(comp_df, use_container_width=True)

        # Normalized bar chart (% difference from non-sanctioned)
        comp_df["% Change"] = ((comp_df["Sanctioned"] - comp_df["Not Sanctioned"]) / comp_df["Not Sanctioned"].abs() * 100).round(1)
        comp_df["Color"] = comp_df.apply(
            lambda r: "#e74c3c" if r["Sanctions Harm?"].startswith("Yes") else "#2ecc71", axis=1)

        fig_pct = go.Figure(go.Bar(
            x=comp_df["Outcome"], y=comp_df["% Change"],
            marker_color=comp_df["Color"],
            text=comp_df["% Change"].apply(lambda x: f"{x:+.1f}%"),
            textposition="outside"
        ))
        fig_pct.add_hline(y=0, line_color="black", line_width=1)
        fig_pct.update_layout(
            title="% Difference in Each Outcome: Sanctioned vs Not Sanctioned<br><sup>Red = sanctions associated with worse outcomes | Green = no apparent harm (unadjusted)</sup>",
            yaxis_title="% Difference (Sanctioned vs Not Sanctioned)",
            height=420
        )
        st.plotly_chart(fig_pct, use_container_width=True)

        # Time-series grid for all outcomes
        st.subheader("Trends Over Time: All Outcomes")
        selected_outcome = st.selectbox(
            "Select outcome to view time trend:",
            [o[0] for o in all_outcomes if o[0] in df.columns],
            format_func=lambda x: x.replace("_"," ").title()
        )
        if selected_outcome in df.columns:
            ts = df.dropna(subset=[selected_outcome]).groupby(["year","sanction_active"])[selected_outcome].mean().reset_index()
            ts["Status"] = ts["sanction_active"].map({0:"Not Sanctioned", 1:"Sanctioned"})
            fig_ts = px.line(ts, x="year", y=selected_outcome, color="Status",
                             color_discrete_map={"Not Sanctioned":"#2196F3","Sanctioned":"#F44336"},
                             title=f"{selected_outcome.replace('_',' ').title()} Over Time by Sanction Status")
            fig_ts.update_layout(height=380)
            st.plotly_chart(fig_ts, use_container_width=True)

        st.info("**Important:** These descriptive differences reflect a mix of sanction effects AND pre-existing country differences (selection bias). See the Advanced Analysis page for causal fixed-effects estimates.")

    with tab2:
        st.subheader("Composite Civilian Well-Being Index")
        st.markdown("""
        **How the index is built:**
        - Combine all 5 dimensions into one score using z-score normalization
        - Invert 'bad' variables (mortality, unemployment, inflation) so higher = better
        - Average the standardized scores → rescale to 0–100

        **Interpretation:** Score of 100 = best observed well-being. Score of 0 = worst.
        """)

        wb_data = data.get("wb_index", pd.DataFrame())
        if not wb_data.empty and "wellbeing_index_100" in wb_data.columns:
            # Metrics
            col1, col2, col3 = st.columns(3)
            not_s_idx = wb_data[wb_data["sanction_active"]==0]["wellbeing_index_100"].mean()
            is_s_idx  = wb_data[wb_data["sanction_active"]==1]["wellbeing_index_100"].mean()
            col1.metric("Not Sanctioned — Avg Index", f"{not_s_idx:.1f}/100")
            col2.metric("Sanctioned — Avg Index", f"{is_s_idx:.1f}/100")
            col3.metric("Gap (unadjusted)", f"{not_s_idx - is_s_idx:.1f} points")

            # Time series
            wb_ts = wb_data.groupby(["year","sanction_active"])["wellbeing_index_100"].mean().reset_index()
            wb_ts["Status"] = wb_ts["sanction_active"].map({0:"Not Sanctioned",1:"Sanctioned"})
            fig_wb = px.line(wb_ts, x="year", y="wellbeing_index_100", color="Status",
                             color_discrete_map={"Not Sanctioned":"steelblue","Sanctioned":"firebrick"},
                             title="Composite Civilian Well-Being Index Over Time (0=worst, 100=best)",
                             labels={"wellbeing_index_100":"Well-Being Index"})
            fig_wb.update_layout(height=400)
            st.plotly_chart(fig_wb, use_container_width=True)

            # Distribution
            wb_data["Status"] = wb_data["sanction_active"].map({0:"Not Sanctioned",1:"Sanctioned"})
            fig_dist = px.histogram(wb_data, x="wellbeing_index_100", color="Status", nbins=40,
                                    barmode="overlay", opacity=0.6,
                                    color_discrete_map={"Not Sanctioned":"steelblue","Sanctioned":"firebrick"},
                                    title="Distribution of Well-Being Index by Sanction Status",
                                    labels={"wellbeing_index_100":"Well-Being Index (0–100)"})
            fig_dist.update_layout(height=350)
            st.plotly_chart(fig_dist, use_container_width=True)
        else:
            st.info("Run milestone3_final.ipynb to generate the composite well-being index.")

    with tab3:
        st.subheader("Sanction Episodes Over Time")

        sanc_yearly = df.groupby("year").agg(
            n_sanctioned=("sanction_active", "sum"),
            pct_sanctioned=("sanction_active", "mean"),
            avg_intensity=("sanction_intensity_index", "mean")
        ).reset_index()

        fig_sanc = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                  subplot_titles=("Number of Sanctioned Countries",
                                                  "Average Sanction Intensity"))
        fig_sanc.add_trace(go.Bar(x=sanc_yearly["year"], y=sanc_yearly["n_sanctioned"],
                                   name="N Sanctioned", marker_color="#F44336"), row=1, col=1)
        fig_sanc.add_trace(go.Scatter(x=sanc_yearly["year"], y=sanc_yearly["avg_intensity"],
                                       name="Avg Intensity", line=dict(color="#FF9800", width=2)),
                            row=2, col=1)
        fig_sanc.update_layout(height=500, title_text="Sanction Trends 1995–2024")
        st.plotly_chart(fig_sanc, use_container_width=True)

        if "sanction_type" in df.columns:
            st.subheader("Sanction Type Distribution")
            type_counts = df[df["sanction_active"]==1]["sanction_type"].value_counts().reset_index()
            type_counts.columns = ["Sanction Type", "Count"]
            fig_type = px.pie(type_counts, values="Count", names="Sanction Type",
                              title="Distribution of Sanction Types",
                              color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig_type, use_container_width=True)

    with tab4:
        st.subheader("Civilian Well-Being by Country (Average, All Years)")
        map_var = st.selectbox("Select variable to map:",
            ["child_mortality_u5","school_enrollment","unemployment_rate","inflation_rate"],
            format_func=lambda x: x.replace("_"," ").title())
        if "country" in df.columns and "country_code" in df.columns and map_var in df.columns:
            country_avg = df.dropna(subset=[map_var]).groupby(["country_code","country"])[map_var].mean().reset_index()
            fig_map = px.choropleth(
                country_avg, locations="country_code", color=map_var, hover_name="country",
                color_continuous_scale="Reds" if map_var=="child_mortality_u5" else "Blues",
                range_color=[0, country_avg[map_var].quantile(0.95)],
                title=f"Average {map_var.replace('_',' ').title()} (All Years)"
            )
            fig_map.update_layout(height=500)
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("Country name/code not available for map view.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4: MODEL RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 Model Results":
    st.title("🤖 Predictive Model Results")
    st.markdown("Comparing three machine learning models: Linear Regression, Random Forest, and Gradient Boosting.")

    # Model comparison table
    if not data["comparison"].empty:
        st.subheader("Model Performance Comparison")
        comp = data["comparison"].copy()
        st.dataframe(comp.style.highlight_max(
            subset=[c for c in comp.columns if "R2" in c], color="lightgreen"
        ).highlight_min(
            subset=[c for c in comp.columns if "RMSE" in c or "MAE" in c], color="lightgreen"
        ), use_container_width=True)

        # Bar chart of R² values
        r2_cols = [c for c in comp.columns if "R2" in c and "Val" in c]
        test_r2_cols = [c for c in comp.columns if "R2" in c and "Test" in c]

        if r2_cols and test_r2_cols:
            fig_r2 = go.Figure()
            fig_r2.add_trace(go.Bar(name="Validation R²", x=comp["Model"], y=comp[r2_cols[0]],
                                    marker_color="#2196F3"))
            fig_r2.add_trace(go.Bar(name="Test R²", x=comp["Model"], y=comp[test_r2_cols[0]],
                                    marker_color="#4CAF50"))
            fig_r2.update_layout(
                title="Validation vs Test R² by Model",
                barmode="group", yaxis_title="R²",
                yaxis=dict(range=[0, 1]), height=400
            )
            st.plotly_chart(fig_r2, use_container_width=True)

    # Feature importance
    if not data["perm_imp"].empty:
        st.subheader("Feature Importance (Random Forest — Permutation Importance)")
        perm = data["perm_imp"].head(15).copy()
        perm["feature_label"] = perm["feature"].str.replace("_", " ").str.title()
        fig_imp = px.bar(
            perm.sort_values("importance_mean"),
            x="importance_mean", y="feature_label",
            error_x="importance_std",
            orientation="h",
            color="importance_mean",
            color_continuous_scale="Oranges",
            title="Top 15 Features by Permutation Importance (Validation Set)",
            labels={"importance_mean": "Permutation Importance", "feature_label": "Feature"}
        )
        fig_imp.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_imp, use_container_width=True)

    # Actual vs Predicted
    if not data["test_preds"].empty:
        st.subheader("Actual vs Predicted Child Mortality (Test Set)")
        preds = data["test_preds"].copy()
        if "actual_child_mortality_u5" in preds.columns and "predicted_child_mortality_u5" in preds.columns:
            preds["Residual"] = preds["actual_child_mortality_u5"] - preds["predicted_child_mortality_u5"]
            preds["AbsResidual"] = preds["Residual"].abs()

            col1, col2 = st.columns(2)
            with col1:
                fig_scatter = px.scatter(
                    preds, x="actual_child_mortality_u5", y="predicted_child_mortality_u5",
                    opacity=0.4, color="AbsResidual",
                    color_continuous_scale="Reds",
                    title="Actual vs Predicted (Test Set)",
                    labels={"actual_child_mortality_u5": "Actual", "predicted_child_mortality_u5": "Predicted"}
                )
                min_val = min(preds["actual_child_mortality_u5"].min(), preds["predicted_child_mortality_u5"].min())
                max_val = max(preds["actual_child_mortality_u5"].max(), preds["predicted_child_mortality_u5"].max())
                fig_scatter.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val],
                                                  mode="lines", name="Perfect Fit", line=dict(color="black", dash="dash")))
                fig_scatter.update_layout(height=400)
                st.plotly_chart(fig_scatter, use_container_width=True)

            with col2:
                # Residuals by year
                if "year" in preds.columns:
                    res_by_year = preds.groupby("year")["Residual"].mean().reset_index()
                    fig_res = px.bar(res_by_year, x="year", y="Residual",
                                     title="Mean Residual by Year (Test Set)",
                                     color="Residual",
                                     color_continuous_scale="RdBu",
                                     color_continuous_midpoint=0)
                    fig_res.add_hline(y=0, line_dash="dash", line_color="black")
                    fig_res.update_layout(height=400)
                    st.plotly_chart(fig_res, use_container_width=True)

    # Model metrics table
    if not data["metrics"].empty:
        st.subheader("Detailed Metrics (Linear Regression Baseline)")
        metrics = data["metrics"].copy()
        st.table(metrics.round(4))


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5: ADVANCED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Advanced Analysis":
    st.title("📈 Advanced Analysis")

    tab1, tab2, tab3 = st.tabs(["Fixed-Effects Regression", "Event Study", "Multi-Outcome Results"])

    with tab1:
        st.subheader("Fixed-Effects Panel Regression Results")
        st.markdown("""
        **What this shows:** The within-country effect of sanctions on child mortality,
        after removing all time-invariant country differences and controlling for global year trends.

        **Interpretation:** Unlike simple OLS, fixed-effects estimation uses only within-country
        variation. This controls for the fact that sanctioned countries may differ systematically
        from non-sanctioned countries (selection bias).
        """)

        if not data["fe_results"].empty:
            fe = data["fe_results"].copy()
            fe_key = fe[fe["Variable"].isin(
                ["sanction_active_w", "sanction_intensity_index_w",
                 "gdp_growth_w", "inflation_rate_w", "conflict_incidence_w",
                 "conflict_intensity_w", "unemployment_rate_w",
                 "log_total_trade_exposure_w", "regime_score_w"]
            )].copy()

            if not fe_key.empty:
                fe_key["Label"] = fe_key["Variable"].str.replace("_w", "").str.replace("_", " ").str.title()
                fe_key["Significant"] = fe_key["P_value"] < 0.05
                fe_key["Color"] = fe_key.apply(
                    lambda r: "Positive (sig)" if r["Coefficient"] > 0 and r["Significant"]
                    else "Negative (sig)" if r["Coefficient"] < 0 and r["Significant"]
                    else "Not significant", axis=1)

                fig_fe = go.Figure()
                for i, row in fe_key.iterrows():
                    color = {"Positive (sig)": "#F44336", "Negative (sig)": "#2196F3", "Not significant": "#9E9E9E"}[row["Color"]]
                    fig_fe.add_trace(go.Scatter(
                        x=[row["CI_low"], row["CI_high"]],
                        y=[row["Label"], row["Label"]],
                        mode="lines", line=dict(color=color, width=3),
                        showlegend=False
                    ))
                    fig_fe.add_trace(go.Scatter(
                        x=[row["Coefficient"]],
                        y=[row["Label"]],
                        mode="markers",
                        marker=dict(color=color, size=10),
                        name=row["Color"],
                        showlegend=i == fe_key.index[0]
                    ))
                fig_fe.add_vline(x=0, line_dash="dash", line_color="black", line_width=1)
                fig_fe.update_layout(
                    title="Fixed-Effects Coefficients with 95% Confidence Intervals",
                    xaxis_title="Coefficient (effect on child mortality per 1,000)",
                    height=500
                )
                st.plotly_chart(fig_fe, use_container_width=True)

                st.dataframe(
                    fe_key[["Label", "Coefficient", "Std_Error", "P_value", "CI_low", "CI_high", "Significant"]].round(4),
                    use_container_width=True
                )
        else:
            st.info("Run the milestone3_final.ipynb notebook first to generate fixed-effects results.")
            st.markdown("The fixed-effects regression will estimate how within-country changes in sanction status affect child mortality, after controlling for GDP growth, inflation, conflict, and year fixed effects.")

    with tab2:
        st.subheader("Event Study: Child Mortality Around Sanction Onset")
        st.markdown("""
        **What this shows:** How average child mortality evolves before and after a country's first sanction episode.

        - **Year 0** = First year of sanctions (onset)
        - **Years −5 to −1** = Pre-sanction trend (flat = good for causal interpretation)
        - **Years +1 to +5** = Post-sanction response
        """)

        if not data["event_study"].empty:
            es = data["event_study"].copy()
            es["normalized"] = es.get("mean_normalized", es.get("mean"))

            fig_es = make_subplots(rows=1, cols=2,
                                    subplot_titles=("Levels", "Normalized to Year −1"))
            # Levels
            fig_es.add_trace(go.Scatter(
                x=es["relative_year"], y=es["ci_high"], fill=None,
                mode="lines", line=dict(width=0), showlegend=False
            ), row=1, col=1)
            fig_es.add_trace(go.Scatter(
                x=es["relative_year"], y=es["ci_low"],
                fill="tonexty", mode="lines", line=dict(width=0),
                fillcolor="rgba(33,150,243,0.2)", name="95% CI"
            ), row=1, col=1)
            fig_es.add_trace(go.Scatter(
                x=es["relative_year"], y=es["mean"],
                mode="lines+markers", line=dict(color="#2196F3", width=2),
                marker=dict(size=8), name="Avg Mortality"
            ), row=1, col=1)
            fig_es.add_vline(x=0, line_dash="dash", line_color="red",
                              annotation_text="Onset", row=1, col=1)

            # Normalized
            if "mean_normalized" in es.columns:
                fig_es.add_trace(go.Scatter(
                    x=es["relative_year"], y=es["ci_high_n"], fill=None,
                    mode="lines", line=dict(width=0), showlegend=False
                ), row=1, col=2)
                fig_es.add_trace(go.Scatter(
                    x=es["relative_year"], y=es["ci_low_n"],
                    fill="tonexty", mode="lines", line=dict(width=0),
                    fillcolor="rgba(255,152,0,0.2)", showlegend=False
                ), row=1, col=2)
                fig_es.add_trace(go.Scatter(
                    x=es["relative_year"], y=es["mean_normalized"],
                    mode="lines+markers", line=dict(color="#FF9800", width=2),
                    marker=dict(size=8), name="Normalized"
                ), row=1, col=2)
                fig_es.add_vline(x=0, line_dash="dash", line_color="red", row=1, col=2)
                fig_es.add_hline(y=0, line_dash="dot", line_color="gray", row=1, col=2)

            fig_es.update_layout(height=450, title_text="Event Study: Child Mortality Dynamics")
            fig_es.update_xaxes(title_text="Years Relative to Sanction Onset")
            st.plotly_chart(fig_es, use_container_width=True)

            with st.expander("View Event Study Data"):
                st.dataframe(es.round(3))
        else:
            st.info("Run milestone3_final.ipynb to generate event study data.")

    with tab3:
        st.subheader("Multi-Outcome Fixed-Effects Results")
        st.markdown("Comparing how sanctions affect child mortality, school enrollment, and unemployment.")

        if not data["multi_outcome"].empty:
            mo = data["multi_outcome"].copy()

            # Filter to sanction_active only for clarity
            mo_sanc = mo[mo["Variable"] == "Sanction Active"].copy() if "Sanction Active" in mo["Variable"].values \
                else mo[mo["Variable"].str.contains("Sanction", na=False)].copy()

            if not mo_sanc.empty:
                fig_mo = px.bar(
                    mo_sanc, x="Outcome", y="Coef", color="Sig",
                    color_discrete_map={"*": "#F44336", "": "#9E9E9E"},
                    error_y=mo_sanc["SE"] * 1.96,
                    title="Sanction Active Effect Across Outcomes (Fixed Effects)<br><sup>Red = statistically significant (p < 0.05)</sup>",
                    labels={"Coef": "FE Coefficient", "Sig": "Significance"}
                )
                fig_mo.add_hline(y=0, line_dash="dash", line_color="black")
                fig_mo.update_layout(height=400)
                st.plotly_chart(fig_mo, use_container_width=True)

            st.dataframe(mo, use_container_width=True)
        else:
            st.info("Run milestone3_final.ipynb to generate multi-outcome results.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6: FINDINGS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Findings":
    st.title("📋 Key Findings and Conclusions")

    st.subheader("Summary of Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Descriptive Findings
        - Sanctioned country-years show **higher average child mortality** than non-sanctioned ones
        - This gap is **descriptive only** — selection bias plays a role
        - Sanctions are concentrated in specific countries with pre-existing vulnerability

        ### Fixed-Effects Findings
        - After controlling for country + year fixed effects, sanction effects become smaller
        - Suggests **selection bias is important**: sanctioned countries were already different
        - Within-country sanction onset coincides with economic stress (inflation, unemployment)
        - The within-country effect is **statistically weaker** than unadjusted comparisons suggest

        ### Event-Study Findings
        - Child mortality in sanctioned countries was already elevated before onset
        - Some evidence of gradual increase post-sanction in certain countries
        - Pre-sanction trends are not flat → parallel trends assumption is imperfect
        """)

    with col2:
        st.markdown("""
        ### Modeling Findings
        | Model | Val R² | Test R² |
        |-------|--------|---------|
        | Linear Regression | ~0.67 | ~0.52 |
        | Random Forest | ~0.81 | ~0.54 |
        | **Gradient Boosting** | **best** | **~0.54** |

        - All three models outperform the naive (mean-prediction) baseline
        - **Top predictors**: female primary enrollment, poverty rate, school enrollment
        - Sanction variables contribute, but are secondary to structural welfare indicators
        - Gradient Boosting is the best predictive model

        ### Multi-Outcome Findings
        - Sanction effects are most visible in child mortality and unemployment
        - School enrollment shows smaller, less consistent sanction associations
        - Trade channel variables (pharma/fuel imports) have moderate predictive power
        """)

    st.markdown("---")
    st.subheader("Variable Selection Justification")

    with st.expander("Why child_mortality_u5 is the best dependent variable"):
        st.markdown("""
        **child_mortality_u5** (under-5 mortality per 1,000 live births) was selected as the primary
        dependent variable for several reasons:

        1. **Multidimensional welfare proxy**: High child mortality reflects lack of food security,
           inadequate healthcare access, poor sanitation, and poverty simultaneously.
        2. **Policy channel sensitivity**: Sanctions that restrict medicine (e.g., pharma imports)
           and humanitarian goods should directly manifest in child health outcomes.
        3. **Data completeness**: Only 9.5% missing vs. 68% missing for poverty_rate and 74% for gini_index.
        4. **Established in literature**: International sanctions studies commonly use child health
           outcomes as civilian welfare proxies (e.g., Weiss et al. 1997).
        5. **Internationally comparable**: WHO/UNICEF methodology makes this measure consistent across countries.
        """)

    with st.expander("Why sanction_active + sanction_intensity_index as treatment variables"):
        st.markdown("""
        The project uses **both** sanction variables together:

        - **sanction_active** (binary): Captures the on/off presence of sanctions.
          Easy to interpret: "did this country face any sanction this year?"
        - **sanction_intensity_index** (continuous 0–1): Captures the degree of economic coercion.
          Sanctions vary enormously — targeted visa bans vs. comprehensive trade embargoes.

        Using both allows the model to detect threshold effects (any sanction) and dose-response
        effects (intensity matters beyond binary presence).
        """)

    with st.expander("Limitations and Caveats"):
        st.markdown("""
        1. **No true random assignment**: Sanctions are imposed for political reasons.
           Countries facing sanctions are different from those that don't — pure causal identification is hard.
        2. **Missing data**: Poverty (68% missing) and Gini (74% missing) limit welfare channel analysis.
        3. **Fixed-effects trade-off**: By removing between-country variation, FE uses only within-country
           changes. Countries with stable sanction regimes contribute little to estimation.
        4. **Reverse causality**: Countries in economic crisis may be both more likely to face sanctions
           AND to have deteriorating welfare.
        5. **Spillover effects**: Neighboring countries of sanctioned economies may be affected,
           violating the stable unit treatment value assumption (SUTVA).
        """)

    st.markdown("---")
    st.success("""
    **Bottom Line:** International sanctions are associated with worse civilian outcomes in sanctioned
    countries. However, rigorous fixed-effects analysis shows that much of the observed gap reflects
    pre-existing differences between sanctioned and non-sanctioned countries rather than a causal
    sanction effect. Honest analysis requires distinguishing correlation from causation — this project
    applies the appropriate methods to draw that distinction.
    """)
