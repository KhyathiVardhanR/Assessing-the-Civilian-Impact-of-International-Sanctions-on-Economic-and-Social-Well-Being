# Assessing the Civilian Impact of International Sanctions on Economic and Social Well-Being

## Project Overview

This project investigates how **international sanctions** affect the welfare of civilian populations.
Rather than studying whether sanctions achieve their political goals, the project asks:
**Do sanctions harm ordinary people, and through what economic channels do these effects operate?**

### Research Question
> How do international sanctions affect civilian economic and social well-being over time,
> through what economic transmission mechanisms do these effects operate, and do these pressures
> coincide with political instability or government turnover?

### Conceptual Framework
```
Sanctions
  → Trade restrictions & financial constraints
  → Import/export contraction (food, medicine, energy)
  → Price instability & macroeconomic stress
  → Poverty & household welfare decline
  → Child health & education outcomes
```

---

## Final Outcome (Milestone 3)

### Deployed Tool
🔗 **Live App:** [https://sanctions-civilian-wellbeing.streamlit.app](https://sanctions-civilian-wellbeing.streamlit.app)

The project is deployed as an interactive **Streamlit dashboard** (`app.py`) that allows users to:
- Explore the country-year panel dataset with filters
- Visualize sanction impacts on child mortality, education, and unemployment
- Compare three machine learning models (Linear Regression, Random Forest, Gradient Boosting)
- Examine fixed-effects regression results (causal inference)
- Explore event-study dynamics around sanction onset
- Review heterogeneous effects by regime type and sanction type

**To run the dashboard locally:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Variable Selection

### Dependent Variable (Primary Target)
**`child_mortality_u5`** — Under-5 child mortality rate per 1,000 live births

Justification:
- Captures food security, healthcare access, sanitation, and poverty simultaneously
- Best data completeness among welfare outcomes (only 9.5% missing)
- Directly sensitive to policy channels targeted by sanctions (medicine, food imports)
- Internationally comparable across countries and years

### Independent Variables (Treatment)
- **`sanction_active`** — Binary indicator (1 = sanctions imposed, 0 = no sanctions)
- **`sanction_intensity_index`** — Continuous 0–1 scale of sanction severity

Using both captures threshold effects (any sanction) and dose-response effects (severity).

### Control Variables
| Variable | Role |
|----------|------|
| `gdp_growth` | Economic performance confounder |
| `inflation_rate` | Price instability indicator |
| `conflict_incidence` | Distinguish sanction effects from war shocks |
| `conflict_intensity` | Severity of armed conflict |
| `regime_score` | Political system type (Polity V) |
| `unemployment_rate` | Labor market conditions |
| `log_total_trade_exposure` | Trade openness |

### Secondary Outcomes
- `school_enrollment` — Human capital investment
- `unemployment_rate` — Labor market impact

---

## Data Sources

| Dataset | Source | Variables | Coverage |
|---------|--------|-----------|----------|
| Sanctions | Global Sanctions Data Base (GSDB) | sanction_active, type, duration, intensity | 1995–2024 |
| Trade | UN Comtrade | oil_exports, pharma_imports, fuel_imports | 1995–2024 |
| Welfare | World Bank WDI | child mortality, enrollment, poverty, GDP | 1995–2024 |
| Political | UCDP / Polity V / Archigos | conflict, regime score | 1995–2024 |

---

## Repository Structure

```
.
├── app.py                          ← Streamlit deployment app (run this to launch dashboard)
├── requirements.txt                ← Python dependencies
├── README.md
│
├── Notebook/
│   ├── milestone1.ipynb            ← Data acquisition & EDA
│   ├── data_wrangling.ipynb        ← Cleaning & feature engineering
│   ├── data_modeling.ipynb         ← Baseline & advanced modeling (M2)
│   ├── data_visualization_static.ipynb  ← Static dashboard (M2)
│   └── milestone3_final.ipynb      ← Final analysis: FE, event study, GB, multi-outcome (M3)
│
├── data/
│   ├── raw/
│   │   ├── sanctions.csv
│   │   ├── trade.csv
│   │   ├── wdi.csv
│   │   └── political.csv
│   └── processed/
│       ├── merged_dataset.csv
│       ├── feature_engineered_dataset.csv
│       ├── model_ready_dataset.csv
│       ├── fe_regression_results.csv       ← Fixed-effects results (M3)
│       ├── multi_outcome_fe_results.csv    ← Multi-outcome FE (M3)
│       ├── three_model_comparison.csv      ← All 3 models compared (M3)
│       ├── event_study_stats.csv           ← Event study data (M3)
│       ├── model_metrics.csv
│       └── [prediction & importance CSVs]
│
├── diary/
│   ├── 01_problem_formulation.txt
│   ├── 02_data_acquisition.txt
│   ├── 03_database_storage.txt
│   ├── 04_data_exploration.txt
│   ├── 05_reflection_next_steps.txt
│   ├── 06_data_cleaning.txt
│   ├── 07_feature_engineering.txt
│   ├── 08_modeling_setup.txt
│   ├── 09_model_evaluation.txt
│   ├── 10_dashboard_reflection.txt
│   ├── 11_fixed_effects_analysis.txt       ← Milestone 3 diary (M3)
│   ├── 12_advanced_modeling.txt            ← Milestone 3 diary (M3)
│   └── 13_final_findings_deployment.txt    ← Milestone 3 diary (M3)
│
└── docs/
    ├── database_schema.png
    └── Data_Dictionary.pdf
```

---

## How to Reproduce

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Notebooks in Order
```
1. Notebook/milestone1.ipynb              # Data acquisition, EDA, database
2. Notebook/data_wrangling.ipynb          # Cleaning, merging, feature engineering
3. Notebook/data_modeling.ipynb           # Linear Regression + Random Forest (M2)
4. Notebook/data_visualization_static.ipynb  # Static dashboard (M2)
5. Notebook/milestone3_final.ipynb        # Fixed-effects, event study, GB, multi-outcome (M3)
```

### Step 3: Launch the Dashboard
```bash
streamlit run app.py
```

---

## Key Findings

Findings come from **5 civilian well-being outcomes** across health, education, gender equity, and economic dimensions, plus a composite index combining all five.

| Dimension | Outcome | Unadjusted Gap | FE Within-Country Effect | Significant? |
|-----------|---------|----------------|--------------------------|--------------|
| Health | child_mortality_u5 | Higher in sanctioned countries | +0.64 per 1,000 | No (p=0.69) |
| Education | school_enrollment | Lower in sanctioned countries | +0.05 pp | No (p=0.97) |
| Gender equity | Girls enrollment | Lower in sanctioned countries | +0.52 pp | No (p=0.67) |
| Economic | unemployment_rate | Higher in sanctioned countries | −0.16 pp | No (p=0.68) |
| Price stability | inflation_rate | Higher in sanctioned countries | +3.37 pp | No (p=0.24) |
| **Composite** | Well-Being Index (0–100) | 94.2 vs 94.8 (≈ no gap) | Near zero | No |

**Core Finding:** After controlling for country fixed effects (which absorbs all pre-existing country-level differences), sanctions have NO statistically significant within-country effect on any of the five well-being outcomes. The unadjusted descriptive gap is driven by **selection bias** — countries targeted by sanctions were already poorer and more vulnerable before sanctions were imposed.

1. **Best predictive model:** Gradient Boosting — Validation R²=0.83, Test R²=0.65
2. **Top predictors:** Female primary enrollment, poverty rate, school enrollment
3. **Event study:** Child mortality declines over the sanction window — tracking the global trend; no sharp break at onset
4. **Policy implication:** Humanitarian relief programs for sanctioned populations need to address pre-existing structural vulnerability, not only the sanctions themselves

---

## Milestone Progress

| Milestone | Status | Key Deliverables |
|-----------|--------|-----------------|
| Milestone 1 | Complete | Problem formulation, data acquisition, SQLite DB, EDA |
| Milestone 2 | Complete | Data wrangling, feature engineering, LR + RF models, static dashboard |
| Milestone 3 | Complete | Fixed-effects regression, event study, Gradient Boosting, Streamlit app |

---

## Heilmeier Catechism

**What are you trying to do?**
Evaluate whether international sanctions cause measurable civilian welfare harm, and through what economic channels.

**How is it done today, and what are the limits?**
Existing research relies on GDP/inflation proxies and simple comparisons without panel identification strategies.

**What is new in your approach?**
Integration of four datasets, fixed-effects panel regression, event-study design, and multi-outcome analysis into a deployed interactive tool.

**Who cares?**
Policymakers, humanitarian organizations, international relations researchers, and civilians in sanctioned countries.

**If successful, what difference will it make?**
A rigorous, reproducible framework for evaluating sanction impacts on civilian populations, moving beyond anecdotal accounts.
