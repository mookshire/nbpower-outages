
import requests
import json

url = "https://services1.arcgis.com/nXhOU3TMjpIZsCx0/arcgis/rest/services/PublicOutageFC_Prod/FeatureServer/0/query"
params = {
    "where": "1=1",
    "outFields": "*",
    "f": "json"
}

response = requests.get(url, params=params)
data = response.json()

# Extract only the relevant fields
extracted = []
for feature in data.get("features", []):
    attr = feature.get("attributes", {})
    extracted.append({
        "customers_affected": attr.get("CustEff"),
        "outages": attr.get("NoOfOutages"),
    })

# Save to outages.json
with open("outages.json", "w") as f:
    json.dump(extracted, f, indent=2)
