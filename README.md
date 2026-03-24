## Assessing the Civilian Impact of International Sanctions on Economic and Social Well-Being

### Heilmeier Catechism – Project Overview

Research Question: 
How do international sanctions affect civilian economic and social well-being over time, through what economic transmission mechanisms do these effects operate, and do these pressures coincide with political instability or government turnover?


1. What are you trying to do?

This project evaluates international sanctions as instruments of economic coercion and examines how their effects are transmitted through civilian economies.

Sanctions are designed to impose economic costs in order to alter government behavior. However, those costs are often absorbed by domestic markets and households. This study investigates whether sanctions generate measurable civilian hardship and whether such hardship coincides with broader economic and political instability.

Rather than relying solely on aggregate GDP or inflation, this research constructs a multidimensional country-year panel dataset to measure the impact of sanctions on:

- Trade in essential goods (food, medicine, energy)
- Price stability and macroeconomic performance
- Poverty and income inequality
- Child health and educational outcomes
- Political instability and leadership turnover

The objective is to empirically trace how external economic pressure propagates through trade channels, affects household welfare, and potentially aligns with political change.


2. How is it done today, and what are the limits of current practice?

Sanctions research traditionally focuses on political effectiveness (e.g., policy compliance or regime change) or examines macroeconomic indicators in isolation. Civilian impacts are frequently discussed descriptively rather than evaluated through structured panel analysis.

Key limitations in existing research include:

- Overreliance on GDP and inflation as proxies for welfare
- Limited integration of trade data as a transmission mechanism
- Weak identification strategies that do not control for armed conflict or global shocks
- Insufficient attention to lagged and heterogeneous effects
- Lack of structured designs linking sanction timing to civilian and political outcomes

This project addresses these gaps by integrating sanctions, trade, macroeconomic, social, and political datasets within a country-year panel framework. The analysis employs fixed-effects models, event-study designs, and conflict controls to strengthen causal interpretation.


# Conceptual Framework

The project is built around the following transmission mechanism:

Sanctions
→ Trade restrictions and financial constraints
→ Import/export contraction (food, medicine, energy)
→ Price instability and macroeconomic stress
→ Poverty and household welfare decline
→ Political instability or leadership turnover

Armed conflict is included as a control variable to distinguish sanction effects from war-related economic shocks.


# Data Sources

The project integrates four primary datasets:

1. Sanctions Data
- Sanction start and end dates
- Type and scope of measures
- Duration and intensity indicators
Source: Global Sanctions Data Base (GSDB)

2. Trade Data
- Food imports
- Medicine imports
- Oil exports
- Fuel imports
Source: UN Comtrade

3. Macroeconomic and Social Indicators
- GDP growth
- Inflation rate
- Unemployment rate
- Poverty rate
- Income inequality (Gini index)
- Under-5 child mortality
- School enrollment
Source: World Bank World Development Indicators (WDI)

4. Political and Conflict Indicators
- Armed conflict incidence and intensity
- Regime type
- Leadership turnover events
Sources: UCDP Armed Conflict Dataset, Polity V, Archigos


# Milestone 1

Milestone 1 establishes the empirical and structural foundation of the project by:

- Refining the theoretical and empirical research framework
- Acquiring and documenting sanctions, trade, macroeconomic, social, and political datasets
- Constructing a relational SQLite database structured by country and year
- Conducting exploratory data analysis to assess data quality and variation
- Developing a comprehensive data dictionary to ensure transparency and reproducibility

At this stage, the focus is on building a structured, replicable panel dataset capable of supporting rigorous econometric modeling.


# Repository Structure

data/raw/ – Raw datasets (sanctions, trade, macroeconomic, social, conflict, political)
data/processed/ – Cleaned and merged country-year panel dataset
database/ – SQLite database files and schema
notebooks/ – Data acquisition, cleaning, and exploratory analysis
diary/ – Milestone documentation, reflections, and data dictionary


# Contribution

This repository provides a transparent and reproducible framework for evaluating how sanctions, as instruments of economic coercion, affect civilian well-being and whether economic hardship coincides with political instability.

By integrating trade channels, welfare indicators, conflict controls, and political outcomes, the project moves beyond simple correlation and toward structured causal analysis appropriate for master’s-level research.
