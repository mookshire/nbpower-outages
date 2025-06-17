import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.nbpower.com/Open/Outages.aspx?lang=en"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", class_="table")
rows = table.find("tbody").find_all("tr")

outages = []
for row in rows:
    cells = row.find_all("td")
    outages.append({
        "region": cells[0].text.strip(),
        "unplanned": cells[1].text.strip(),
        "customers": cells[2].text.strip(),
        "planned": cells[3].text.strip(),
    })

with open("outages.json", "w") as f:
    json.dump(outages, f, indent=2)

print("[SUCCESS] Scraped and saved to outages.json")

