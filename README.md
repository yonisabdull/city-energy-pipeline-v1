# UK Local Authority Emissions Pipeline

This project builds a complete, reproducible workflow for cleaning, transforming, storing, and analysing UK local authority greenhouse gas (GHG) emissions data. The aim was to work with a real public dataset and build a small but structured pipeline that moves from raw input to meaningful analysis and visual outputs.

The pipeline includes basic data cleaning, schema checks, type enforcement, database loading, SQL analysis, bar-chart reporting, and a UK emissions density map.

I chose emissions data because it's a real-world issue where data actually matters. Local authorities make policy decisions using datasets like this, so it felt meaningful to work with. I've also been really interested in sustainability ever since I worked as a Sustainability Coordinator, so exploring a dataset connected to local environmental impact felt like a natural fit.

---

## Project overview

This pipeline:

- Loads the raw DESNZ local authority emissions dataset  
- Validates expected schema  
- Cleans and standardises all fields  
- Enforces strict numeric and string types  
- Creates derived metrics such as per-capita emissions and emissions per km²  
- Loads cleaned data into a SQLite database  
- Runs SQL queries for insights  
- Generates bar charts to answer key questions  
- Builds a geospatial choropleth map using UK local authority boundaries  

---

## Folder structure

city-energy-pipeline/
├── src/
│   ├── etl/
│   │   ├── clean_ghg.py
│   │   └── load_to_sql.py
│   └── analysis/
│       ├── plots.py
│       ├── maps.py
│       └── query_sql.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── geo/
│
├── outputs/
├── requirements.txt
└── README.md
---

## Data sources

Download the following before running:

### 1. DESNZ Local Authority GHG Emissions  
https://www.gov.uk/government/statistics/uk-local-authority-and-regional-greenhouse-gas-emissions-statistics-2005-to-2023
Save as: data/raw/ghg_emissions.csv

### 2. UK Local Authority Boundary GeoJSON  
https://github.com/martinjc/UK-GeoJSON  
Save as: data/geo/uk_lad.geojson

---
---

## How to run the pipeline

### Install dependencies
pip install -r requirements.txt

### 1. Clean the raw DESNZ file under this here
python src/etl/clean_ghg.py
Produces:
data/processed/ghg_emissions_clean.csv

### 2. Load that cleaned data into SQLite
python src/etl/load_to_sql.py
Produces:
energy_usage.db

### 3. Generate bar-chart outputs
python src/analysis/plots.py

Outputs (saved to /outputs):
- top_total_latest.png  
- top_per_capita_latest.png  
- top_density_latest.png  
- sector_neath_port_talbot.png  

### 4. Generate the UK emissions density map

python src/analysis/maps.py
Outputs:
outputs/uk_emissions_density_map.png


---

## What each step does

### Cleaning (clean_ghg.py)
- Checked required columns  
- Renamed columns to snake_case  
- Trimmed whitespace  
- Converted blanks to NaN  
- Casted numeric columns (float64)  
- Casted IDs/text to string  
- Converted year to Int64  
- Added per-capita + density metrics  
- Removed bad or incomplete rows  

### Database loading (load_to_sql.py)
- Created SQLite database  
- Wrote the cleaned dataset into a table  
- Replaced existing table on each run  

### SQL analysis (plots.py)
- Pulled metrics from SQLite  
- Identified highest emitters  
- Identified highest per-capita emitters  
- Identified highest emissions density  
- Extracted sector breakdowns  

### Mapping (maps.py)
- Read local authority boundary GeoJSON  
- Merged emissions density with boundary shapes  
- Used quantile binning for readable colour ranges  
- Exported a UK-wide emissions density choropleth  

---

## Outputs

All final outputs are saved under: /outputs

This includes:

- Bar charts (PNG)  
- UK emissions density map (PNG)  

---

## What I learned 

- Handling real public datasets with messy formatting  
- Enforcing schemas and data types in Python  
- Using SQLite for lightweight data storage  
- Writing SQL queries for analysis on incredibly large datasets
- Creating clear bar-chart visualisations  
- Performing geospatial merges and building choropleths  
- Structuring a simple end-to-end local data pipeline  

---

## Next steps (Maybe)

- Add basic unit tests for data cleaning  
- Add config file for paths  
- Add a CLI wrapper for single-command execution  
- Add forecasting for selected authorities  
- Build a small dashboard version

---

If running the pipeline in order:

python src/etl/clean_ghg.py

python src/etl/load_to_sql.py

python src/analysis/plots.py

python src/analysis/maps.py
