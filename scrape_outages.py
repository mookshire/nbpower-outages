import json
from playwright.sync_api import sync_playwright

# NB Power district codes and region names
districts = [
    ("0110", "York"),
    ("0210", "K.V."),
    ("0130", "Carleton"),
    ("0240", "Charlotte"),
    ("0220", "Kings"),
    ("0510", "Kent"),
    ("0520", "Moncton"),
    ("0310", "Miramichi"),
    ("0140", "Grand Falls"),
    ("0410", "Acadian"),
    ("0420", "Heat"),
    ("0320", "Restigouche"),
    ("0610", "Sackville"),
    ("0620", "Shediac")
]

# Helper function to extract numbers from a selector (or return -1)
def safe_extract(page, selector):
    try:
        return int(page.locator(selector).inner_text().strip().replace(",", ""))
    except:
        return -1

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    data = []

    for code, name in districts:
        print(f"▶ Visiting {name} district {code}")
        try:
            page.goto(f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={code}&il=0", timeout=60000)
            page.wait_for_selector("#ctl00_cphMain_lblOutageCount", timeout=30000)

            outages = safe_extract(page, "#ctl00_cphMain_lblOutageCount")
            customers = safe_extract(page, "#ctl00_cphMain_lblCustAffect")

            print(f"✔ {name}: {outages} outages, {customers} customers affected")
        except Exception as e:
            print(f"❌ {name} FAILED: {e}")
            outages = -1
            customers = -1

        data.append({
            "region": name,
            "outages": outages,
            "customers_affected": customers
        })

    browser.close()

    with open("outages.json", "w") as f:
        json.dump(data, f, indent=2)

    print("✅ Done writing outages.json")
