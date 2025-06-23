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
        browser = p.chromium.launch(headless=True, timeout=60000)
        page = browser.new_page()

        # Set English
        print("Setting language...")
        try:
            page.goto("https://www.nbpower.com/Open/Outages.aspx?lang=en", timeout=20000)
            print("Language set to English.")
        except TimeoutError:
            print("Language page timed out — continuing anyway.")

        # Loop through regions
        for name, code in regions:
            url = f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={code}&il=0"
            print(f">>> Fetching {name} - {url}")

            try:
                page.goto(url, timeout=25000)

                outage_text = page.inner_text("#ctl00_cphMain_lblOutageCount")
                cust_text = page.inner_text("#ctl00_cphMain_lblCustAffected")

                print(f"{name}: Found '{outage_text}', '{cust_text}'")

                outages = int(outage_text.split()[0]) if outage_text else -1
                customers = int(cust_text.split()[0].replace(",", "")) if cust_text else 0

            except TimeoutError:
                print(f"⚠️ Timeout on {name}")
                outages = -1
                customers = -1
            except Exception as e:
                print(f"❌ Error in {name}: {str(e)}")
                outages = -1
                customers = -1

            results.append({
                "region": name,
                "outages": outages,
                "customers_affected": customers
            })

        browser.close()
        print("Browser closed.")

    # Save JSON
    try:
        with open("outages.json", "w") as f:
            json.dump(results, f, indent=2)
        print("✅ outages.json written successfully.")
    except Exception as e:
        print(f"❌ Failed to write JSON: {str(e)}")

if __name__ == "__main__":
    scrape()
