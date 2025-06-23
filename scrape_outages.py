import requests
from bs4 import BeautifulSoup
import json
import re

districts = {
    "0110": "York",
    "0120": "K.V.",
    "0130": "Carleton",
    "0140": "Charlotte",
    "0150": "Kings",
    "0160": "Kent",
    "0170": "Moncton",
    "0180": "Miramichi",
    "0190": "Grand Falls",
    "0200": "Acadian",
    "0210": "Heat",
    "0220": "Restigouche",
    "0230": "Sackville",
    "0240": "Shediac",
}

base_url = "https://www.nbpower.com/Open/SearchOutageResults.aspx?district={}&il=0"

headers = {
    "User-Agent": "Mozilla/5.0"
}

outage_data = []

for district_code, region_name in districts.items():
    url = base_url.format(district_code)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", class_="rgMasterTable")
        if not table:
            outages = 0
            customers = 0
        else:
            rows = table.find_all("tr", class_=re.compile("rgRow|rgAltRow"))
            outages = len(rows)

            customers = 0
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 5:
                    count_str = cells[4].text.strip().replace(",", "")
                    try:
                        customers += int(count_str)
                    except ValueError:
                        pass

        outage_data.append({
            "region": region_name,
            "outages": outages,
            "customers_affected": customers
        })
    except Exception as e:
        print(f"Error fetching data for {region_name} ({district_code}): {e}")
        outage_data.append({
            "region": region_name,
            "outages": None,
            "customers_affected": None,
            "error": str(e)
        })

with open("outages.json", "w") as f:
    json.dump(outage_data, f, indent=2)

