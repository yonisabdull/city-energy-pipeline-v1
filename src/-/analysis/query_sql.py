import sqlite3
DB_PATH = "data/energy_usage.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

query = """
SELECT local_authority, sum(territorial_emissions_ktco2e) as total_emissions
FROM energy_usage
WHERE year = (SELECT MAX(year) FROM energy_usage)
GROUP BY local_authority
ORDER BY total_emissions DESC
LIMIT 10;
"""
rows = cursor.execute(query).fetchall()
    
print("QUERY RESULTS:")
for row in rows:
    print(row)

conn.close()