import json
from playwright.sync_api import sync_playwright, TimeoutError

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
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Step 1: Set language to English
        print("Setting language to English...")
        try:
            page.goto("https://www.nbpower.com/Open/Outages.aspx?lang=en", timeout=30000)
        except TimeoutError:
            print("Language bypass timeout – continuing anyway.")

        # Step 2: Scrape each district
        for name, code in regions:
            url = f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={code}&il=0"
            print(f"Scraping {name} from {url}")
            try:
                page.goto(url, timeout=30000)

                outage_text = page.inner_text("#ctl00_cphMain_lblOutageCount")
                cust_text = page.inner_text("#ctl00_cphMain_lblCustAffected")

                outages = int(outage_text.split()[0]) if outage_text else -1
                customers = int(cust_text.split()[0].replace(",", "")) if cust_text else 0

            except TimeoutError:
                print(f"Timeout while loading {url}")
                outages = -1
                customers = -1
            except Exception as e:
                print(f"Error in {name}: {str(e)}")
                outages = -1
                customers = -1

            results.append({
                "region": name,
                "outages": outages,
                "customers_affected": customers
            })

        browser.close()
        print("Browser closed.")

    with open("outages.json", "w") as f:
        json.dump(results, f, indent=2)
        print("outages.json written successfully.")

if __name__ == "__main__":
    scrape()
