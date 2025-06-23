import json
from datetime import datetime
from playwright.sync_api import sync_playwright

regions = [
    ("York", "0110"),
    ("K.V.", "0210"),
    ("Carleton", "0130"),
    ("Charlotte", "0240"),
    ("Kings", "0220"),
    ("Kent", "0510"),
    ("Moncton", "0520"),
    ("Miramichi", "0420"),
    ("Grand Falls", "0140"),
    ("Acadian", "0440"),
    ("Heat", "0410"),
    ("Restigouche", "0430"),
    ("Sackville", "0530"),
    ("Shediac", "0540"),
]

def scrape():
    print(">>> STARTING REGION SCRAPE")
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(locale='en-CA')
        context.set_default_timeout(15000)
        page = context.new_page()

        for name, code in regions:
            url = f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={code}&il=0"
            print(f"→ {name}: Visiting {url}")
            try:
                page.goto(url)
                page.wait_for_selector("#ctl00_cphMain_lblOutageCount")
                outage = page.inner_text("#ctl00_cphMain_lblOutageCount")
                customers = page.inner_text("#ctl00_cphMain_lblCustAffected")
                print(f"✓ {name}: {outage}, {customers}")
                results.append({
                    "region": name,
                    "outages": int(outage.split()[0]),
                    "customers_affected": int(customers.split()[0].replace(",", ""))
                })
            except Exception as e:
                print(f"⚠️ Failed for {name}: {e}")
                results.append({
                    "region": name,
                    "outages": -1,
                    "customers_affected": -1
                })

        browser.close()

    results.append({"timestamp": datetime.utcnow().isoformat() + "Z"})

    try:
        with open("outages.json", "w") as f:
            json.dump(results, f, indent=2)
        print("✅ JSON written and saved.")
    except Exception as e:
        print(f"❌ Failed to write JSON: {e}")

    print(">>> SCRAPE DONE")

if __name__ == "__main__":
    scrape()
