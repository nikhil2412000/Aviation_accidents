aviation-accidents-analysis

Data analysis and visualization project for understanding global aviation accident patterns using Python, ETL pipelines, and statistical insights.

Aviation Accidents Analysis – ETL, Visualization & Insights

This project focuses on analyzing global aviation accident data using a complete ETL pipeline, detailed visualizations, and structured insights. It supports identifying accident trends across countries, operators, categories, aircraft types, and time periods, enabling data-driven decision-making and reporting.

📊 Overview

The dataset includes aviation accidents recorded across several countries along with details such as date, operator, aircraft type, fatalities, location, and accident category.
The objective of this analysis is to clean, transform, visualize, and derive insights that can support aviation safety reviews and reporting.

🚀 Key Features

Performed data cleaning, normalization, and validation on the raw dataset.

Implemented a full ETL pipeline (Load → Clean → Analyze → Visualize).

Generated interactive and static visualizations including world maps, bar charts, treemaps, and heatmaps.

Extracted 9 key insights related to countries, operators, aircraft types, and fatality trends.

Created a slide deck summarizing findings for easy presentation.

Produced a cleaned dataset ready for further modeling or reporting.

🧩 Methodology

Data Loading (Excel → Pandas DataFrame)

Data Cleaning & Standardization

Fix column names

Handle missing data

Convert dates

Extract year

Create derived fields (e.g., damage_type)

Exploratory Data Analysis & Visualization

Top accident locations

Global accident distribution

Operator patterns

Category-based accident behavior

Insight Generation

Fatality correlations

Deadliest aircraft types

Operator safety index

Slide Deck Creation for final presentation

📍 Visualizations Included

Top 15 Countries by Accidents

Interactive World Accident Map

Operator Treemap (Country → Operator)

Accident Category vs Damage Type Heatmap

Additional supporting plots (distribution, counts, etc.)

🧠 Technologies Used

Python

Pandas, NumPy

Matplotlib, Seaborn

Plotly Express

PyCountry

Jupyter Notebook / Python Scripts

📈 Insights Generated
Insight	Description
Top Countries	Identified the 15 countries with the most accidents
Year–Fatalities Correlation	Weak or moderate correlation patterns
Deadliest Aircraft Types	Aircraft with highest per-accident fatality rates
Operator Fatality Rankings	Operators with the highest total fatalities
Safety Index	Fatalities per 100 accidents per operator
Category Dominance	Most frequent accident category per country
