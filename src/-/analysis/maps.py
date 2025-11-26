from pathlib import Path
import sqlite3

import geopandas as gpd
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Set paths
DB_PATH = "data/energy_usage.db"
MAP_PATH = "data/geo/uk_lad.geojson"
OUTPUT_PATH = Path("outputs/uk_emissions_density_map.png")


def get_df(query: str, params=None) -> pd.DataFrame:
    """Ran SQL and returned DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


def load_emissions_density() -> pd.DataFrame:
    """Aggregated emissions to density per authority."""
    query = """
        WITH latest_year AS (SELECT MAX(year) AS y FROM energy_usage)
        SELECT
            local_authority,
            SUM(emissions_within_la_scope_ktco2e) * 1000.0
            / MAX(area_km2) AS density
        FROM energy_usage, latest_year
        WHERE year = latest_year.y
        GROUP BY local_authority;
    """
    return get_df(query)


def main():
    # Loaded boundaries
    map_df = gpd.read_file(MAP_PATH)

    # Simplified geometry for plotting
    map_df["geometry"] = map_df["geometry"].simplify(0.005, preserve_topology=True)

    # Loaded emissions density
    em_df = load_emissions_density()

    # Merged map with emissions
    merged = map_df.merge(
        em_df,
        left_on="LAD24NM",
        right_on="local_authority",
        how="left",
    )

    # Capped extreme density values
    merged["density_capped"] = merged["density"].clip(upper=5000)

    # Ensured outputs folder existed
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Drew choropleth map
    fig, ax = plt.subplots(figsize=(8, 10))
    merged.plot(
        column="density_capped",
        cmap="OrRd",
        scheme="quantiles",
        k=5,
        legend=True,
        linewidth=0.3,
        edgecolor="black",
        missing_kwds={"color": "lightgrey", "label": "No data"},
        ax=ax,
        legend_kwds={
            "loc": "lower left",
            "title": "tCO₂e per km²",
        },
    )

    ax.set_title(
        "UK local authorities – emissions density (tCO₂e per km², latest year)\n"
        "Quantile classes, values capped at 5000",
        fontsize=12,
    )
    ax.set_axis_off()

    # Saved figure
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved improved map to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()