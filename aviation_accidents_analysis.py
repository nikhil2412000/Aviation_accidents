# ===========================
#  AVIATION ACCIDENTS ANALYSIS
# ===========================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pycountry


# ============================================
# STEP 1: LOAD DATA FROM FILE
# ============================================

def load_data(file_path):
    """
    Load the aviation accidents Excel file
    """
    print(f" Loading data from: {file_path}")

    df = pd.read_excel(file_path)

    print(f" Loaded {len(df)} rows and {len(df.columns)} columns")
    return df


# ============================================
# STEP 2: CLEAN THE DATA
# ============================================

def clean_data(df):
    """
    Clean and prepare the data for analysis
    """
    print("\n Cleaning data...")

    # Make column names lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Fix incorrect column names
    df = df.rename(columns={
        "air-craft_type": "aircraft_type",
        "registration_name/mark": "registration",
        "fatilites": "fatalities"
    })

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing values with 'Unknown'
    df['aircraft_type'] = df['aircraft_type'].fillna('Unknown')
    df['operator'] = df['operator'].fillna('Unknown')
    df['country'] = df['country'].fillna("Unknown")
    df['category'] = df['category'].fillna("Unknown")

    # Convert fatalities to numbers (replace errors with 0)
    df['fatalities'] = pd.to_numeric(df['fatalities'], errors='coerce').fillna(0)

    # Convert date column and extract year
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year

    # Clean country names (remove extra spaces, make proper case)
    df['country'] = df['country'].str.strip().str.title()

    # Create damage type: 'Hull Loss' if fatalities > 0, else 'Repairable'
    df['damage_type'] = df['fatalities'].apply(lambda x: 'Hull Loss' if x > 0 else 'Repairable')

    print(f"✅ Data cleaned! Final dataset has {len(df)} rows")
    print(f" Date range: {df['year'].min()} to {df['year'].max()}")

    return df


# ============================================
# HELPER: CONVERT COUNTRY NAME TO CODE
# ============================================

def get_country_code(country_name):
    """
    Convert country name to 3-letter code (for maps)
    Example: 'United States' -> 'USA'
    """
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except:
        return None


# ============================================
# STEP 3: CREATE VISUALIZATIONS
# ============================================

def create_top_countries_chart(df):
    """
    Chart 1: Bar chart showing countries with most accidents
    """
    print("\n Creating Top Countries chart...")

    # Get top 15 countries
    top15 = df['country'].value_counts().head(15)

    # Create the chart
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top15.values, y=top15.index, palette='Reds_r')
    plt.title('Top 15 Countries by Aviation Accidents', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Accidents')
    plt.ylabel('Country')

    # Add numbers on bars
    for i, v in enumerate(top15.values):
        plt.text(v + 5, i, str(v), color='black', va='center', fontweight='bold')

    plt.tight_layout()
    plt.show()

    # Print percentage share
    percentage = (top15.sum() / len(df)) * 100
    print(f" Top 15 countries = {percentage:.1f}% of all accidents")


def create_world_map(df):
    """
    Chart 2: Interactive world map showing accident distribution
    """
    print("\n Creating World Map...")

    # Count accidents per country
    country_data = df['country'].value_counts().reset_index()
    country_data.columns = ['country', 'accidents']

    # Get country codes for mapping
    country_data['country_code'] = country_data['country'].apply(get_country_code)
    country_data = country_data.dropna(subset=['country_code'])

    # Create interactive map
    fig = px.scatter_geo(
        country_data,
        locations='country_code',
        color='accidents',
        hover_name='country',
        size='accidents',
        projection='natural earth',
        title='Global Distribution of Aviation Accidents',
        color_continuous_scale='Reds'
    )
    fig.show()
    print(" World map created!")


def create_operator_treemap(df):
    """
    Chart 3: Treemap showing operators grouped by country
    """
    print("\n Creating Operator Treemap...")

    # Group by country and operator
    operator_data = (
        df.groupby(['country', 'operator'])
        .size()
        .reset_index(name='accident_count')
        .sort_values(by='accident_count', ascending=False)
    )

    # Create treemap
    fig = px.treemap(
        operator_data,
        path=['country', 'operator'],
        values='accident_count',
        color='accident_count',
        color_continuous_scale='Reds',
        title='Aviation Accidents by Country and Operator'
    )
    fig.show()
    print(" Treemap created!")


def create_category_heatmap(df):
    """
    Chart 4: Heatmap showing accident categories vs damage type
    """
    print("\n Creating Category Heatmap...")

    # Create pivot table
    pivot = df.pivot_table(
        index='category',
        columns='damage_type',
        aggfunc='size',
        fill_value=0
    )

    # Create heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="Reds")
    plt.title("Accident Categories vs Damage Type", fontsize=14, fontweight='bold')
    plt.xlabel("Damage Type")
    plt.ylabel("Accident Category")
    plt.tight_layout()
    plt.show()
    print(" Heatmap created!")


def create_all_charts(df):
    """
    Master function: Creates all 4 visualizations
    """
    print("\n" + "=" * 60)
    print(" CREATING ALL VISUALIZATIONS")
    print("=" * 60)

    create_top_countries_chart(df)
    create_world_map(df)
    create_operator_treemap(df)
    create_category_heatmap(df)

    print("\n All visualizations completed!")


# ============================================
# STEP 4: GENERATE INSIGHTS
# ============================================

def print_insight_1(df):
    """Insight 1: What % of accidents are in top 15 countries?"""
    print("\n INSIGHT 1: Top 15 Countries Share")
    top15_count = df['country'].value_counts().head(15).sum()
    percentage = (top15_count / len(df)) * 100
    print(f"   Top 15 countries account for {percentage:.2f}% of all accidents")


def print_insight_2(df):
    """Insight 2: Which countries have the most accidents?"""
    print("\n INSIGHT 2: Top 5 Countries with Most Accidents")
    print(df['country'].value_counts().head(5))


def print_insight_3(df):
    """Insight 3: Is there a correlation between year and fatalities?"""
    print("\n INSIGHT 3: Correlation Between Fatalities and Year")
    corr = df[['fatalities', 'year']].corr()
    print(corr)


def print_insight_4(df):
    """Insight 4: What's the biggest accident category per country?"""
    print("\n INSIGHT 4: Largest Accident Category per Top Country")
    top15_countries = df['country'].value_counts().head(15).index
    temp = df[df['country'].isin(top15_countries)]
    segment = temp.groupby(['country', 'category']).size().reset_index(name='count')
    segment = segment.loc[segment.groupby('country')['count'].idxmax()]
    print(segment)


def print_insight_5(df):
    """Insight 5: Which country has the most accidents?"""
    print("\n INSIGHT 5: Country with Most Accidents")
    country = df['country'].value_counts().idxmax()
    count = df['country'].value_counts().max()
    print(f"   {country}: {count} accidents")


def print_insight_6(df):
    """Insight 6: What are the most common aircraft types?"""
    print("\n INSIGHT 6: Top 10 Most Common Aircraft Types")
    print(df['aircraft_type'].value_counts().head(10))


def print_insight_7(df):
    """Insight 7: Which operators have the highest fatalities?"""
    print("\n INSIGHT 7: Operators with Highest Total Fatalities")
    operator_fatalities = df.groupby('operator')['fatalities'].sum().sort_values(ascending=False).head(10)
    print(operator_fatalities)


def print_insight_8(df):
    """Insight 8: Which aircraft types are deadliest per accident?"""
    print("\n INSIGHT 8: Deadliest Aircraft Types (Fatality Rate)")
    aircraft_stats = df.groupby('aircraft_type').agg(
        total_accidents=('aircraft_type', 'count'),
        total_fatalities=('fatalities', 'sum')
    )
    aircraft_stats['fatality_rate'] = aircraft_stats['total_fatalities'] / aircraft_stats['total_accidents']
    print(aircraft_stats.sort_values('fatality_rate', ascending=False).head(10))


def print_insight_9(df):
    """Insight 9: Operator safety index (fatalities per 100 accidents)"""
    print("\n INSIGHT 9: Operator Safety Index (min 5 accidents)")
    operator_stats = df.groupby('operator').agg(
        accidents=('operator', 'count'),
        fatalities=('fatalities', 'sum')
    )
    operator_stats['safety_index'] = (operator_stats['fatalities'] / operator_stats['accidents']) * 100
    operator_stats = operator_stats[operator_stats['accidents'] >= 5]
    print(operator_stats.sort_values('safety_index', ascending=False).head(10))


def print_all_insights(df):
    """
    Master function: Prints all 9 insights
    """
    print("\n" + "=" * 60)
    print("GENERATING ALL INSIGHTS")
    print("=" * 60)

    print_insight_1(df)
    print_insight_2(df)
    print_insight_3(df)
    print_insight_4(df)
    print_insight_5(df)
    print_insight_6(df)
    print_insight_7(df)
    print_insight_8(df)
    print_insight_9(df)

    print("\n All insights completed!")


# ============================================
# MAIN ETL PIPELINE
# ============================================

def run_etl(file_path):
    """
    Main function that runs everything:
    1. Load data
    2. Clean data
    3. Create visualizations
    4. Print insights

    Input: file_path (example: "aviation_accidents.xlsx")
    Output: cleaned DataFrame
    """
    print("=" * 60)
    print("AVIATION ACCIDENTS ANALYSIS - STARTING...")
    print("=" * 60)

    # Step 1: Load the data
    df = load_data(file_path)

    # Step 2: Clean the data
    df = clean_data(df)

    # Step 3: Create all visualizations
    create_all_charts(df)

    # Step 4: Print all insights
    print_all_insights(df)

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

    return df


# ============================================
# RUN THE PROGRAM
# ============================================

if __name__ == "__main__":
    # Set your file path here
    file_path = "aviation_accidents in countries - aviation_accidents.xlsx"

    # Run the complete analysis
    cleaned_data = run_etl(file_path)

    # Now you have the cleaned data available for further analysis
    print(f"\n Cleaned dataset has {len(cleaned_data)} records")