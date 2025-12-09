# aviation-accidents-analysis

Data analysis and visualization project for understanding global aviation accident patterns using Python, ETL pipelines, and statistical insights.

## Aviation Accidents Analysis – ETL, Visualization & Insights

This project focuses on analyzing global aviation accident data using a complete ETL pipeline, detailed visualizations, and structured insights. It supports identifying accident trends across countries, operators, categories, aircraft types, and time periods, enabling data-driven decision-making and reporting.

# Overview

The dataset includes aviation accidents recorded across several countries along with details such as date, operator, aircraft type, fatalities, location, and accident category.
The objective of this analysis is to clean, transform, visualize, and derive insights that can support aviation safety reviews and reporting.

# Key Features

Performed data cleaning, normalization, and validation on the raw dataset.
Implemented a full ETL pipeline (Load → Clean → Analyze → Visualize).
Generated interactive and static visualizations including world maps, bar charts, treemaps, and heatmaps.
Extracted 9 key insights related to countries, operators, aircraft types, and fatality trends.
Created a slide deck summarizing findings for easy presentation.
Produced a cleaned dataset ready for further modeling or reporting.

# Methodology

## 1. Data Loading

Loaded Excel dataset using Pandas
Initial inspection of rows and columns

## 2. Data Cleaning & Standardization

Standardized column names
Removed duplicates
Filled missing values
Converted dates and extracted year
Cleaned country names
Converted fatalities to numeric values
Added derived column: damage_type (Hull Loss / Repairable)

## 3. Exploratory Data Analysis & Visualization

Accident distribution across countries
Global mapping of accident hotspots
Operator-level accident patterns
Category-wise accident behavior

## 4. Insight Generation

Correlation between year and fatalities
Identification of deadliest aircraft types
Operator safety comparison
Dominant accident categories by country

## 5. Slide Deck Creation

Summarized results into a visually structured presentation

# Visualizations Included

Top 15 Countries by Accidents
Interactive World Accident Map
Operator Treemap (Country → Operator)
Accident Category vs Damage Type Heatmap
Additional supporting plots (distribution, counts, etc.)

# Technologies Used

Python
Pandas, NumPy
Matplotlib, Seaborn
Plotly Express
PyCountry
Jupyter Notebook / Python Scripts

# Insights Generated

| Insight                         | Description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| **Top Countries**               | Identified the 15 countries with the highest accident counts |
| **Year–Fatalities Correlation** | Weak/mild correlation between fatalities and year            |
| **Deadliest Aircraft Types**    | Aircraft types with the highest fatality rate                |
| **Operator Fatality Rankings**  | Operators with the highest total fatalities                  |
| **Safety Index**                | Fatalities per 100 accidents per operator                    |
| **Category Dominance**          | Most common accident category per country                    |

