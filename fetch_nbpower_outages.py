import requests
import json

url = "https://services1.arcgis.com/nXhKU3TMjpIZsCx0/arcgis/rest/services/PublicOutageFC_Prod/FeatureServer/0/query"
params = {
    "where": "1=1",
    "outFields": "*",
    "f": "json"
}

response = requests.get(url, params=params)
data = response.json().get("features", [])

extracted = []
for feature in data:
    attr = feature.get("attributes", {})
    extracted.append({
        "customers_affected": attr.get("CustEff"),
        "outages": attr.get("NoOfOutages")
    })

with open("outages.json", "w") as f:
    json.dump(extracted, f, indent=2)
