import json
from playwright.sync_api import sync_playwright

# List of districts and their URLs
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
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for name, code in regions:
            url = f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={code}&il=0"
            page.goto(url, timeout=60000)

            try:
                outage_text = page.inner_text("#ctl00_cphMain_lblOutageCount")
                cust_text = page.inner_text("#ctl00_cphMain_lblCustAffected")

                # Extract numbers (fallback to -1 if not found)
                outages = int(outage_text.split()[0]) if outage_text else -1
                customers = int(cust_text.split()[0].replace(",", "")) if cust_text else 0
            except:
                outages = -1
                customers = 0

            results.append({
                "region": name,
                "outages": outages,
                "customers_affected": customers
            })

        browser.close()

    with open("outages.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    scrape()
