# Assessing the Civilian Impact of International Sanctions on Economic and Social Well-Being

[![Live App](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?logo=streamlit&logoColor=white)](https://sanctions-civilian-wellbeing.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Course](https://img.shields.io/badge/Course-Introduction%20to%20Data%20Science-green)](https://www.ufl.edu/)

> **Live App:** [https://sanctions-civilian-wellbeing.streamlit.app](https://sanctions-civilian-wellbeing.streamlit.app)

---

## What this project is about

Sanctions get imposed on countries all the time — but the debate is usually about whether they work politically. We wanted to ask a different question: **do ordinary people actually get hurt?**

We pulled together data from four sources (World Bank, UN Comtrade, GSDB, UCDP/Polity V) covering 1995–2024, built a panel dataset of ~7,800 country-year observations, and ran a bunch of models to see whether being under sanctions moves the needle on things like child mortality, school enrollment, and inflation.

The short answer: **the raw numbers make sanctioned countries look worse, but once you control for which countries actually get sanctioned (they were already poorer), the within-country effect basically disappears.** The story is more about pre-existing vulnerability than the sanctions themselves.

---

## The data science side

We used child mortality (under-5 deaths per 1,000 births) as our main outcome — it's a good proxy for food access, healthcare, and poverty all at once, and it had the fewest missing values (~9.5%).

Our models, in order of complexity:
- Linear Regression (baseline)
- Random Forest
- Gradient Boosting ← best performer (Test R² = 0.65)

For causal inference, we ran **fixed-effects panel regression** (within-country estimator) and an **event study** around sanction onset. Neither showed a statistically significant effect.

**Control variables:** GDP growth, inflation, conflict incidence and intensity, regime type (Polity V), unemployment, trade exposure.

---

## Key findings

| Outcome | FE Effect | p-value |
|---------|-----------|---------|
| Child mortality | +0.64 per 1,000 | 0.69 |
| School enrollment | +0.05 pp | 0.97 |
| Girls enrollment | +0.52 pp | 0.67 |
| Unemployment | −0.16 pp | 0.68 |
| Inflation | +3.37 pp | 0.24 |

None of these are significant. The top predictors in our ML models were female primary enrollment, poverty rate, and school enrollment — not sanction status itself.

The event study also showed no sharp change in child mortality at the point sanctions were imposed. The gap between sanctioned and non-sanctioned countries in the raw data is largely a selection effect — countries that get sanctioned were already struggling.

---

## Data sources

| Dataset | Source | What we used it for |
|---------|--------|---------------------|
| Sanctions | Global Sanctions Data Base (GSDB) | sanction timing, type, intensity |
| Trade | UN Comtrade | oil/pharma/fuel imports & exports |
| Welfare | World Bank WDI | child mortality, enrollment, GDP, poverty |
| Political | UCDP / Polity V / Archigos | conflict data, regime scores |

---

## Dashboard

The Streamlit app has 6 pages:

| Page | What's on it |
|------|-------------|
| Overview | Research question, dataset summary, methodology |
| Data Explorer | Filter and explore the full dataset interactively |
| Sanction Impact | Side-by-side comparisons across sanctions status |
| Model Results | LR vs. Random Forest vs. Gradient Boosting |
| Advanced Analysis | Fixed-effects regression, event study, multi-outcome |
| Findings | What we concluded and why it matters |

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Repo structure

```
.
├── app.py                               ← Streamlit dashboard
├── requirements.txt
│
├── Notebook/
│   ├── milestone1.ipynb                 ← EDA and data acquisition
│   ├── data_wrangling.ipynb             ← Cleaning and feature engineering
│   ├── data_modeling.ipynb              ← LR + Random Forest
│   ├── data_visualization_static.ipynb  ← Static plots
│   └── milestone3_final.ipynb           ← Fixed-effects, event study, Gradient Boosting
│
├── data/
│   ├── raw/                             ← Source CSVs
│   └── processed/                       ← Cleaned and model-ready data
│
├── diary/                               ← Weekly decision logs (13 entries)
│
└── docs/
    ├── database_schema.png
    └── Data_Dictionary.pdf
```

---

## To reproduce

```bash
# Install dependencies
pip install -r requirements.txt

# Run notebooks in order:
# milestone1.ipynb → data_wrangling.ipynb → data_modeling.ipynb
# → data_visualization_static.ipynb → milestone3_final.ipynb

# Launch the app
streamlit run app.py
```
