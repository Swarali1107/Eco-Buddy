import pathway as pw
import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ecobuddy"]
collection = db["reports"]

# Fetch reports from DB
def fetch_reports():
    reports = list(collection.find({}))
    return [
        {
            "latitude": float(r["latitude"]),
            "longitude": float(r["longitude"]),
            "status": r["status"]
        }
        for r in reports
        if r.get("latitude") and r.get("longitude")
    ]

# Create Pathway table
class ReportSchema(pw.Schema):
    latitude: float
    longitude: float
    status: str

reports_data = fetch_reports()

table = pw.debug.table_from_pandas(
    pw.pandas.DataFrame(reports_data)
)

# Assign intensity based on status
table = table.with_columns(
    intensity = pw.apply(
        lambda s: 1.0 if s == "Pending"
        else 0.7 if s == "In Progress"
        else 0.3,
        table.status
    )
)

# Group nearby points (round to grid)
table = table.with_columns(
    lat_grid = pw.apply(lambda x: round(x, 3), table.latitude),
    lng_grid = pw.apply(lambda x: round(x, 3), table.longitude),
)

heatmap = (
    table.groupby(table.lat_grid, table.lng_grid)
    .reduce(
        lat = pw.reducers.first(table.lat_grid),
        lng = pw.reducers.first(table.lng_grid),
        intensity = pw.reducers.sum(table.intensity)
    )
)

# Output JSON
result = heatmap.to_pandas()

print(result.to_json(orient="records"))
