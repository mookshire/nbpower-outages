import requests
from bs4 import BeautifulSoup
import json

# Map region nicknames to NB Power district codes
districts = {
    "York": "0110",
    "K.V.": "0210",
    "Carleton": "0130",
    "Charlotte": "0240",
    "Kings": "0220",
    "Kent": "0510",
    "Moncton": "0520",
    "Miramichi": "0310",
    "Grand Falls": "0140",
    "Acadian": "0410",
    "Heat": "0420",
    "Restigouche": "0320",
    "Sackville": "0610",
    "Shediac": "0620"
}

base_url = "https://www.nbpower.com/Open/SearchOutageResults.aspx?district={}&il=0"

headers = {
    "User-Agent": "Mozilla/5.0"
}

results = []

for region, code in districts.items():
    url = base_url.format(code)
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        outage_count = soup.find("span", id="ctl00_cphMain_lblOutageCount")
        customer_count = soup.find("span", id="ctl00_cphMain_lblCustAffect")

        outages = int(outage_count.text.strip()) if outage_count else -1
        customers = int(customer_count.text.strip().replace(",", "")) if customer_count else -1

        results.append({
            "region": region,
            "outages": outages,
            "customers_affected": customers
        })

    except Exception as e:
        results.append({
            "region": region,
            "outages": -1,
            "customers_affected": -1
        })

# Write to outages.json
with open("outages.json", "w") as f:
    json.dump(results, f, indent=2)

