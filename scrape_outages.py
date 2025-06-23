import json
from playwright.sync_api import sync_playwright

REGIONS = {
    "York": "0110",
    "K.V.": "0120",
    "Carleton": "0130",
    "Charlotte": "0140",
    "Kings": "0150",
    "Kent": "0210",
    "Moncton": "0220",
    "Miramichi": "0230",
    "Grand Falls": "0240",
    "Acadian": "0410",
    "Heat": "0420",
    "Restigouche": "0430",
    "Sackville": "0440",
    "Shediac": "0450",
}

def scrape():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        
        # Inject lang cookie to bypass language screen
        context.add_cookies([{
            "name": "lang",
            "value": "en",
            "domain": ".nbpower.com",
            "path": "/",
            "httpOnly": False,
            "secure": True,
            "sameSite": "Lax"
        }])

        page = context.new_page()

        for region_name, code in REGIONS.items():
            url = f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={code}&il=0"
            try:
                page.goto(url, timeout=60000)
                html = page.content()

                # Check for language page fallback
                if "Français" in html and "English" in html:
                    raise Exception("Language selector appeared")

                page.wait_for_selector("#ctl00_cphMain_UpdatePanel1", timeout=10000)
                table_text = page.inner_text("#ctl00_cphMain_UpdatePanel1")

                outages = customers = -1
                for line in table_text.splitlines():
                    if "Number of Active Outages" in line:
                        outages = int(line.split(":")[-1].strip())
                    elif "Number of Customers Affected" in line:
                        customers = int(line.split(":")[-1].strip())

                results.append({
                    "region": region_name,
                    "outages": outages,
                    "customers_affected": customers
                })

            except Exception as e:
                print(f"Error with region {region_name}: {e}")
                results.append({
                    "region": region_name,
                    "outages": -1,
                    "customers_affected": -1
                })

        context.close()
        browser.close()

    with open("outages.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    scrape()
