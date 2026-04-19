# Assessing the Civilian Impact of International Sanctions on Economic and Social Well-Being

[![Live App](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?logo=streamlit&logoColor=white)](https://sanctions-civilian-wellbeing.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Course](https://img.shields.io/badge/Course-Introduction%20to%20Data%20Science-green)](https://www.ufl.edu/)

> **Live Dashboard:** [https://sanctions-civilian-wellbeing.streamlit.app](https://sanctions-civilian-wellbeing.streamlit.app)

---

## Project Overview

This project investigates how **international sanctions** affect the welfare of civilian populations. Rather than studying whether sanctions achieve their political goals, the project asks: **Do sanctions harm ordinary people, and through what economic channels do these effects operate?**

### Research Question
> How do international sanctions affect civilian economic and social well-being over time, through what economic transmission mechanisms do these effects operate, and do these pressures coincide with political instability or government turnover?

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

## Deployed Tool

The project is deployed as an interactive **Streamlit dashboard** with 6 pages:

| Page | Description |
|------|-------------|
| Overview | Research framework, methodology, dataset summary |
| Data Explorer | Interactive filters across 7,820 country-year observations |
| Sanction Impact | Descriptive comparisons across 5 civilian well-being dimensions |
| Model Results | Linear Regression, Random Forest, and Gradient Boosting comparison |
| Advanced Analysis | Fixed-effects regression, event study, multi-outcome results |
| Findings | Key conclusions, variable justification, policy implications |

**To run locally:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Variable Selection

### Dependent Variable
**`child_mortality_u5`** — Under-5 child mortality rate per 1,000 live births

Chosen because it captures food security, healthcare access, sanitation, and poverty simultaneously, has the best data completeness (only 9.5% missing), and is directly sensitive to the humanitarian channels that sanctions target.

### Treatment Variables
- **`sanction_active`** — Binary indicator (1 = sanctions imposed, 0 = no sanctions)
- **`sanction_intensity_index`** — Continuous 0–1 scale of sanction severity

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
- `SE.PRM.NENR.FE` — Girls primary enrollment (gender equity)
- `inflation_rate` — Price stability

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
├── app.py                               ← Streamlit dashboard (6 pages)
├── requirements.txt                     ← Python dependencies
├── README.md
│
├── Notebook/
│   ├── milestone1.ipynb                 ← Data acquisition & EDA
│   ├── data_wrangling.ipynb             ← Cleaning & feature engineering
│   ├── data_modeling.ipynb              ← Linear Regression + Random Forest (M2)
│   ├── data_visualization_static.ipynb  ← Static dashboard (M2)
│   └── milestone3_final.ipynb           ← Fixed-effects, event study, Gradient Boosting (M3)
│
├── data/
│   ├── raw/                             ← Source CSVs (GSDB, Comtrade, WDI, UCDP)
│   └── processed/                       ← Cleaned, merged, and model-ready datasets
│
├── diary/                               ← Weekly decision logs (13 entries)
│
└── docs/
    ├── database_schema.png
    └── Data_Dictionary.pdf
```

---

## How to Reproduce

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run notebooks in order
#    milestone1.ipynb → data_wrangling.ipynb → data_modeling.ipynb
#    → data_visualization_static.ipynb → milestone3_final.ipynb

# 3. Launch the dashboard
streamlit run app.py
```

---

## Key Findings

| Dimension | Outcome | FE Within-Country Effect | Significant? |
|-----------|---------|--------------------------|--------------|
| Health | child_mortality_u5 | +0.64 per 1,000 | No (p=0.69) |
| Education | school_enrollment | +0.05 pp | No (p=0.97) |
| Gender equity | Girls enrollment | +0.52 pp | No (p=0.67) |
| Economic | unemployment_rate | −0.16 pp | No (p=0.68) |
| Price stability | inflation_rate | +3.37 pp | No (p=0.24) |
| **Composite** | Well-Being Index | Near zero | No |

**Core Finding:** After controlling for country fixed effects, sanctions have no statistically significant within-country effect on any of the five well-being outcomes. The unadjusted descriptive gap is driven by **selection bias** — sanctioned countries were already poorer and more vulnerable before sanctions were imposed.

- **Best model:** Gradient Boosting — Validation R²=0.83, Test R²=0.65
- **Top predictors:** Female primary enrollment, poverty rate, school enrollment
- **Event study:** No sharp break in child mortality at sanction onset
- **Policy implication:** Humanitarian programs should address pre-existing structural vulnerability, not only the sanctions themselves

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
