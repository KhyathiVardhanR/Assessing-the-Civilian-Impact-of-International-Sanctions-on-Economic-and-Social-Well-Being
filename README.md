# Assessing the Civilian Impact of International Sanctions on Economic and Social Well-Being

[![Live App](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?logo=streamlit&logoColor=white)](https://sanctions-civilian-wellbeing.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Course](https://img.shields.io/badge/Course-Introduction%20to%20Data%20Science-green)](https://www.ufl.edu/)

> **Live App:** [https://sanctions-civilian-wellbeing.streamlit.app](https://sanctions-civilian-wellbeing.streamlit.app)

---

## Overview

Sanctions are frequently imposed as a foreign policy tool — but the conversation around them tends to focus on whether they work politically. This project takes a different angle: **what happens to ordinary people?**

We built a panel dataset of ~7,800 country-year observations (1995–2024) by combining data from the World Bank, UN Comtrade, the Global Sanctions Database, and UCDP/Polity V. Using that, we examined whether sanctions exposure moves outcomes like child mortality, school enrollment, and inflation — and through what channels those effects might operate.

The headline result: **sanctioned countries look worse in raw comparisons, but once you account for which countries get sanctioned in the first place (they were already more vulnerable), the within-country effect is not statistically significant.** The gap in outcomes is largely a pre-existing structural difference, not a sanctions effect.

---

## Methodology

We used **under-5 child mortality** (deaths per 1,000 live births) as the primary outcome. It captures food security, healthcare access, and household poverty simultaneously, and had the lowest missing data rate (~9.5%) of any outcome we considered.

Three models were trained and compared:

- Linear Regression — baseline
- Random Forest
- Gradient Boosting — best performer (Validation R² = 0.83, Test R² = 0.65)

For causal identification, we used **fixed-effects panel regression** (within-country estimator, demeaning approach) and an **event study** around sanction onset. Secondary outcomes — school enrollment, girls' primary enrollment, unemployment, and inflation — were tested in a multi-outcome specification.

**Control variables:** GDP growth, inflation rate, conflict incidence and intensity, regime type (Polity V), unemployment rate, log trade exposure.

---

## Key Findings

| Outcome | Fixed-Effects Estimate | p-value |
|---------|----------------------|---------|
| Child mortality | +0.64 per 1,000 | 0.69 |
| School enrollment | +0.05 pp | 0.97 |
| Girls' enrollment | +0.52 pp | 0.67 |
| Unemployment | −0.16 pp | 0.68 |
| Inflation | +3.37 pp | 0.24 |

None of these estimates reach statistical significance. The top predictors in the ML models were female primary enrollment, poverty rate, and school enrollment — not sanction status itself. The event study showed no sharp shift in child mortality at sanction onset.

The descriptive gap between sanctioned and non-sanctioned countries is real, but it reflects **selection** — countries that get sanctioned were already in worse shape before sanctions were imposed.

---

## Data Sources

| Dataset | Source | Variables |
|---------|--------|-----------|
| Sanctions | Global Sanctions Data Base (GSDB) | Sanction timing, type, intensity |
| Trade | UN Comtrade | Oil, pharmaceutical, and fuel trade flows |
| Welfare | World Bank WDI | Child mortality, enrollment, GDP, poverty |
| Political | UCDP / Polity V / Archigos | Conflict data, regime scores |

---

## Interactive Dashboard

The app is deployed on Streamlit Community Cloud and has 6 pages:

| Page | Description |
|------|-------------|
| Overview | Research question, dataset summary, methodology |
| Data Explorer | Filter and explore the full dataset interactively |
| Sanction Impact | Comparisons across sanction status for 5 outcomes |
| Model Results | Linear Regression vs. Random Forest vs. Gradient Boosting |
| Advanced Analysis | Fixed-effects regression, event study, multi-outcome results |
| Findings | Conclusions, variable justification, policy implications |

**Run locally:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Project Structure

```
.
├── app.py                               ← Streamlit dashboard (6 pages)
├── requirements.txt
│
├── Notebook/
│   ├── milestone1.ipynb                 ← Data acquisition and EDA
│   ├── data_wrangling.ipynb             ← Cleaning and feature engineering
│   ├── data_modeling.ipynb              ← Linear Regression + Random Forest
│   ├── data_visualization_static.ipynb  ← Static visualizations
│   └── milestone3_final.ipynb           ← Fixed-effects, event study, Gradient Boosting
│
├── data/
│   ├── raw/                             ← Source CSVs (GSDB, Comtrade, WDI, UCDP)
│   └── processed/                       ← Cleaned and model-ready datasets
│
├── diary/                               ← Weekly decision logs (13 entries)
│
└── docs/
    ├── database_schema.png
    └── Data_Dictionary.pdf
```

---

## Running the Notebooks

The analysis is split across five notebooks that should be run in order:

```bash
pip install -r requirements.txt
jupyter notebook
```

1. `milestone1.ipynb` — data acquisition, SQLite database setup, initial EDA
2. `data_wrangling.ipynb` — cleaning, merging, feature engineering
3. `data_modeling.ipynb` — Linear Regression and Random Forest
4. `data_visualization_static.ipynb` — static dashboard with widgets *(run all cells to activate interactive views)*
5. `milestone3_final.ipynb` — fixed-effects regression, event study, Gradient Boosting
