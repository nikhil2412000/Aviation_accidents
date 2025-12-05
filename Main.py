# ===========================
#  AVIATION ACCIDENTS ANALYSIS
# ===========================

# IMPORT REQUIRED LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pycountry

# ---------------------------------------------
# SECTION 1 — LOAD & CLEAN THE DATA
# ---------------------------------------------

df = pd.read_excel('aviation_accidents in countries - aviation_accidents.xlsx')

# Fix column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Correct wrong column names
df = df.rename(columns={
    "air-craft_type": "aircraft_type",
    "registration_name/mark": "registration",
    "fatilites": "fatalities"
})

# Remove duplicates
df = df.drop_duplicates()

# Missing value handling
df['aircraft_type'] = df['aircraft_type'].fillna('Unknown')
df['operator'] = df['operator'].fillna('Unknown')
df['country'] = df['country'].fillna("Unknown")
df['category'] = df['category'].fillna("Unknown")

# Convert fatalities to numeric
df['fatalities'] = pd.to_numeric(df['fatalities'], errors='coerce').fillna(0)

# Convert date to datetime and extract year
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year

# Standardize country names
df['country'] = df['country'].str.strip().str.title()

# Add damage type column
df['damage_type'] = df['fatalities'].apply(lambda x: 'Hull Loss' if x > 0 else 'Repairable')

# ---------------------------------------------
# SECTION 2 — DATA VISUALIZATIONS
# ---------------------------------------------

# -----------------------------
# CHART 1 — Top 15 Accident Countries
# -----------------------------
print(len(df))
print(df['year'].min())
print(df['year'].max())
plt.figure(figsize=(12, 6))
top15 = df['country'].value_counts().head(15)
#
sns.barplot(x=top15.values, y=top15.index, palette='Reds_r')
plt.title('Top 15 Countries by Total Number of Aviation Accidents', fontsize=14)
plt.xlabel('Number of Accidents')
plt.ylabel('Country')

for i, v in enumerate(top15.values):
    plt.text(v + 5, i, str(v), color='black', va='center', fontweight='bold')

plt.tight_layout()
plt.show()
#
# # % Share of Top 15
top15_share = (top15.sum() / len(df)) * 100
print(f"Top 15 countries account for {top15_share:.2f}% of all recorded aviation accidents.")
#
#
#
# # CHART 2 — Global Accident Map
# # -----------------------------
#
# # Convert country names to ISO codes
def get_country_code(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except:
        return None

country_accidents = df['country'].value_counts().reset_index()
country_accidents.columns = ['country', 'accidents']
country_accidents['country_code'] = country_accidents['country'].apply(get_country_code)
country_accidents = country_accidents.dropna(subset=['country_code'])

fig = px.scatter_geo(
    country_accidents,
    locations='country_code',
    color='accidents',
    hover_name='country',
    size='accidents',
    projection='natural earth',
    title='Global Distribution of Aviation Accidents (1919–2022)',
    color_continuous_scale='Reds'
)
fig.show()


# -----------------------------
# CHART 3 — Operator Treemap
# -----------------------------
operator_data = (
    df.groupby(['country', 'operator'])
      .size()
      .reset_index(name='accident_count')
      .sort_values(by='accident_count', ascending=False)
)

fig = px.treemap(
    operator_data,
    path=['country', 'operator'],
    values='accident_count',
    color='accident_count',
    color_continuous_scale='Reds',
    title='Treemap of Operators by Country – Aviation Accidents'
)
fig.show()


# -----------------------------
# CHART 4 — Category vs Damage Heatmap
# -----------------------------
pivot = df.pivot_table(
    index='category',
    columns='damage_type',
    aggfunc='size',   # FIXED: counts accidents correctly
    fill_value=0
)

plt.figure(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt="d", cmap="Reds")
plt.title("Heatmap of Accident Categories vs Damage Type")
plt.xlabel("Damage Type")
plt.ylabel("Accident Category")
plt.tight_layout()
plt.show()


# ---------------------------------------------
# SECTION 3 — INSIGHTS & ANALYSIS
# ---------------------------------------------

print("\nINSIGHT 1 — % Share of Top 15 Accident Countries")
total_incidents = len(df)
top15_total = df['country'].value_counts().head(15).sum()
print("Top 15 share:", round((top15_total / total_incidents) * 100, 2), "%")


print("\nINSIGHT 2 — Countries with Highest Accidents")
print(df['country'].value_counts().head(5))
#
#
print("\nINSIGHT 3 — Correlation (Fatalities vs Year)")
corr = df[['fatalities', 'year']].corr()
print(corr)
#
#
print("\nINSIGHT 4 — Largest Accident Segment per Top Country")
top15_countries = df['country'].value_counts().head(15).index
temp = df[df['country'].isin(top15_countries)]
segment = temp.groupby(['country', 'category']).size().reset_index(name='count')
segment = segment.loc[segment.groupby('country')['count'].idxmax()]
print(segment)
#
#
print("\nINSIGHT 5 — Country with Most Accidents")
print(df['country'].value_counts().idxmax(),
      df['country'].value_counts().max())


print("\nINSIGHT 6 — Most Common Aircraft Types")
print(df['aircraft_type'].value_counts().head(10))
#
#
print("\nINSIGHT 7 — Operators with Highest Fatalities")
operator_fatalities = df.groupby('operator')['fatalities'].sum().sort_values(ascending=False).head(10)
print(operator_fatalities)
#
#
print("\nINSIGHT 8 — Deadliest Aircraft Types (Fatality Rate)")
aircraft_stats = df.groupby('aircraft_type').agg(
    total_accidents=('aircraft_type', 'count'),
    total_fatalities=('fatalities', 'sum')
)
aircraft_stats['fatality_rate'] = aircraft_stats['total_fatalities'] / aircraft_stats['total_accidents']
print(aircraft_stats.sort_values('fatality_rate', ascending=False).head(10))
#
#
print("\nINSIGHT 9 — Operator Safety Index (Fatalities per 100 Accidents)")
operator_stats = df.groupby('operator').agg(
    accidents=('operator', 'count'),
    fatalities=('fatalities', 'sum')
)
operator_stats['safety_index'] = (operator_stats['fatalities'] / operator_stats['accidents']) * 100
operator_stats = operator_stats[operator_stats['accidents'] >= 5]
print(operator_stats.sort_values('safety_index', ascending=False).head(10))
