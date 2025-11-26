from pathlib import Path
import sqlite3

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DB_PATH = "data/energy_usage.db"
OUT_DIR = Path("outputs")


def fetch_df(query: str) -> pd.DataFrame:
    """Ran SQL and returned DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def save(fig, name: str) -> None:
    """Saved figure to outputs."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / name, dpi=300, bbox_inches="tight")
    plt.close(fig)


def top_emitters():
    # Got top emitting authorities
    q = """
        SELECT local_authority,
               SUM(emissions_within_la_scope_ktco2e) AS total_ktco2e
        FROM energy_usage
        GROUP BY local_authority
        ORDER BY total_ktco2e DESC
        LIMIT 10;
    """
    df = fetch_df(q)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(df["local_authority"], df["total_ktco2e"])
    ax.set_title("Top 10 emitting authorities")
    ax.set_xlabel("Emissions within LA scope (kt CO₂e)")
    ax.invert_yaxis()

    save(fig, "top_emitters.png")


def top_density():
    # Got highest emissions per km²
    q = """
        SELECT local_authority,
               SUM(emissions_within_la_scope_ktco2e) * 1000.0 / MAX(area_km2) AS density
        FROM energy_usage
        GROUP BY local_authority
        ORDER BY density DESC
        LIMIT 10;
    """
    df = fetch_df(q)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(df["local_authority"], df["density"])
    ax.set_title("Highest emissions density")
    ax.set_xlabel("tCO₂e per km²")
    ax.invert_yaxis()

    save(fig, "top_density.png")


def top_per_capita():
    # Got highest per-capita emitters
    q = """
        SELECT local_authority,
               SUM(territorial_emissions_ktco2e) * 1000.0
               / (AVG(mid_year_population_thousands) * 1000.0) AS per_capita
        FROM energy_usage
        GROUP BY local_authority
        HAVING per_capita IS NOT NULL
        ORDER BY per_capita DESC
        LIMIT 10;
    """
    df = fetch_df(q)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(df["local_authority"], df["per_capita"])
    ax.set_title("Highest per-capita emissions")
    ax.set_xlabel("tCO₂e per person")
    ax.invert_yaxis()

    save(fig, "top_per_capita.png")


def main():
    top_emitters()
    top_density()
    top_per_capita()
    print("Saved bar charts.")


if __name__ == "__main__":
    main()