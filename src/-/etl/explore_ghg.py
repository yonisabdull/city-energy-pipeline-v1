import pandas as pd
from pathlib import Path

# Paths to raw and cleaned data
RAW_PATH = Path("data/raw/ghg_emissions.csv")
CLEAN_PATH = Path("data/processed/ghg_emissions_clean.csv")  # name it whatever you like


def main():
    # Loaded the raw CSV
    df = pd.read_csv(RAW_PATH)

    # Double-Check the raw file 
    required_columns = [
        "Country",
        "Country Code",
        "Region",
        "Region Code",
        "Second Tier Authority",
        "Local Authority",
        "Local Authority Code",
        "Calendar Year",
        "LA GHG Sector",
        "LA GHG Sub-sector",
        "Greenhouse gas",
        "Territorial emissions (kt CO2e)",
        "Emissions within the scope of influence of LAs (kt CO2)",
        "Mid-year Population (thousands)",
        "Area (km2)",
    ]

    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # 3. Renaming to snake_case
    rename_map = {
        "Country": "country",
        "Country Code": "country_code",
        "Region": "region",
        "Region Code": "region_code",
        "Second Tier Authority": "second_tier_authority",
        "Local Authority": "local_authority",
        "Local Authority Code": "local_authority_code",
        "Calendar Year": "year",
        "LA GHG Sector": "la_ghg_sector",
        "LA GHG Sub-sector": "la_ghg_sub_sector",
        "Greenhouse gas": "greenhouse_gas",
        "Territorial emissions (kt CO2e)": "territorial_emissions_ktco2e",
        "Emissions within the scope of influence of LAs (kt CO2)": "emissions_within_la_scope_ktco2e",
        "Mid-year Population (thousands)": "mid_year_population_thousands",
        "Area (km2)": "area_km2",
    }
    df = df.rename(columns=rename_map)

    # Retyping that data
    schema = {
        "country": "string",
        "country_code": "string",
        "region": "string",
        "region_code": "string",
        "second_tier_authority": "string",
        "local_authority": "string",
        "local_authority_code": "string",
        "year": "Int64",  # pandas nullable integer
        "la_ghg_sector": "string",
        "la_ghg_sub_sector": "string",
        "greenhouse_gas": "string",
        "territorial_emissions_ktco2e": "float64",
        "emissions_within_la_scope_ktco2e": "float64",
        "mid_year_population_thousands": "float64",
        "area_km2": "float64",
    }

    # Keeping only the columns we care about
    df = df[list(schema.keys())]

    # Strip whitespace and empty to NaN
    text_columns = [
        "country",
        "country_code",
        "region",
        "region_code",
        "second_tier_authority",
        "local_authority",
        "local_authority_code",
        "la_ghg_sector",
        "la_ghg_sub_sector",
        "greenhouse_gas",
    ]

    df[text_columns] = (
        df[text_columns]
        .apply(lambda col: col.astype("string").str.strip())
    )

    df[text_columns] = df[text_columns].replace(r"^\s*$", pd.NA, regex=True)

    # Coerce numeric columns
    numeric_columns = [
        "territorial_emissions_ktco2e",
        "emissions_within_la_scope_ktco2e",
        "mid_year_population_thousands",
        "area_km2",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Coerce year as numeric too
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    # Dropped rows missing identifiers or year for SQL
    df = df.dropna(subset=["local_authority", "local_authority_code", "year"])

    # Drop obviously bad values
    df = df.dropna(
        subset=["territorial_emissions_ktco2e", "emissions_within_la_scope_ktco2e"],
        how="all",
    )

    # Enforce final schema types, now that bad values are handled
    df = df.astype(schema)

    # Creating metrics for analysis

    # Per-capita emissions (tonnes CO2e per person)
    df["territorial_emissions_per_capita_tco2e"] = (
        df["territorial_emissions_ktco2e"] * 1000
        / (df["mid_year_population_thousands"] * 1000)
    )

    # Emissions per square kilometre (tonnes CO2e per km^2)
    df["emissions_within_scope_per_km2_tco2e"] = (
        df["emissions_within_la_scope_ktco2e"] * 1000
        / df["area_km2"]
    )

    # Avoid infinities
    df.replace([float("inf"), float("-inf")], pd.NA, inplace=True)

    # Sort for easier queries
    df = df.sort_values(["local_authority", "year", "la_ghg_sector"])

    print("Cleaned shape:", df.shape)
    print(df.dtypes)

    # Save cleaned data
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)
    print(f"Saved cleaned data to {CLEAN_PATH}")


if __name__ == "__main__":
    main()