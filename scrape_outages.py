import json import time from playwright.sync_api import sync_playwright

Districts to scrape

DISTRICTS = { "York": "0110", "K.V.": "0210", "Carleton": "0130", "Charlotte": "0240", "Kings": "0220", "Kent": "0510", "Moncton": "0520", "Miramichi": "0310", "Grand Falls": "0140", "Acadian": "0410", "Heat (Chaleur)": "0420", "Restigouche": "0320", "Sackville": "0610", "Shediac": "0620" }

BASE_URL = "https://www.nbpower.com/Open/SearchOutageResults.aspx?district={}&il=0"

def scrape_district(playwright, name, code): browser = playwright.chromium.launch() page = browser.new_page() url = BASE_URL.format(code) print(f"▶ Visiting {name} district {code}")

try:
    page.goto(url, timeout=60000)

    # Check if we're still stuck on the language selection page
    if "ReturnUrl" in page.url or "Language" in page.content():
        print(f"❌ {name} FAILED: Still on language page")
        return {"region": name, "outages": -1, "customers_affected": -1}

    # Wait up to 30 seconds for the outage data
    page.wait_for_selector("#ctl00_cphMain_lblOutageCount", timeout=30000)
    outages = int(page.query_selector("#ctl00_cphMain_lblOutageCount").inner_text())
    customers = int(page.query_selector("#ctl00_cphMain_lblCustAffectedCount").inner_text())

    print(f"✅ {name} OK: {outages} outages, {customers} customers affected")
    return {"region": name, "outages": outages, "customers_affected": customers}

except Exception as e:
    print(f"❌ {name} FAILED: {e}")
    return {"region": name, "outages": -1, "customers_affected": -1}

finally:
    browser.close()

def main(): results = [] with sync_playwright() as p: for name, code in DISTRICTS.items(): results.append(scrape_district(p, name, code)) time.sleep(1)  # Brief pause to avoid hammering the server

with open("outages.json", "w") as f:
    json.dump(results, f, indent=2)
print("✅ Done writing outages.json")

if name == "main": main()

