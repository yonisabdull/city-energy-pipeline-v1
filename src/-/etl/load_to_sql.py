import pandas as pd
import sqlite3
from pathlib import Path

CLEAN_PATH = Path("data/processed/ghg_emissions_clean.csv")
DB_PATH = Path("data/energy_usage.db")
TABLE_NAME = "energy_usage"

def main():
    # 1. Load cleaned dataset
    df = pd.read_csv(CLEAN_PATH)
    print(f"Loaded cleaned data from: {CLEAN_PATH}")

    # 2. Ensure database directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 3. Connect to SQLite database (creates file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    print(f"Connected to database: {DB_PATH}")

    # 4. Load DataFrame into SQL table
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    print(f"Data loaded into table: {TABLE_NAME}")

    # 5. Close connection
    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()