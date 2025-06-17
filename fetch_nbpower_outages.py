import requests
import json
from collections import defaultdict

url = "https://services1.arcgis.com/nXhKU3TMjpIZsCx0/arcgis/rest/services/PublicOutageFC_Prod/FeatureServer/1/query"
params = {
    "where": "1=1",
    "outFields": "*",
    "f": "json"
}

response = requests.get(url, params=params)
data = response.json()

# Group outages by region name
regions = defaultdict(lambda: {"outages": 0, "customers_affected": 0})

for feature in data.get("features", []):
    attr = feature.get("attributes", {})
    region = attr.get("RegionName", "Unknown")
    regions[region]["outages"] += attr.get("NoOfOutages", 0)
    regions[region]["customers_affected"] += attr.get("CustEff", 0)

# Convert to clean list
output = [
    {
        "region": region,
        "outages": info["outages"],
        "customers_affected": info["customers_affected"]
    }
    for region, info in regions.items()
]

# Save to file
with open("outages.json", "w") as f:
    json.dump(output, f, indent=2)
