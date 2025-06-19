import json
from playwright.sync_api import sync_playwright

# Map of region name to NB Power district URL
REGIONS = [
    ("York", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0110&il=0"),
    ("K.V.", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0210&il=0"),
    ("Carleton", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0130&il=0"),
    ("Charlotte", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0240&il=0"),
    ("Kings", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0220&il=0"),
    ("Kent", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0510&il=0"),
    ("Moncton", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0520&il=0"),
    ("Miramichi", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0420&il=0"),
    ("Grand Falls", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0140&il=0"),
    ("Acadian", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0440&il=0"),
    ("Chaleur", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0410&il=0"),
    ("Restigouche", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0430&il=0"),
    ("Sackville", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0530&il=0"),
    ("Shediac", "https://www.nbpower.com/Open/SearchOutageResults.aspx?district=0540&il=0")
]

def scrape():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for name, url in REGIONS:
            page.goto(url)

            # If redirected to language screen, click English
            if "lang" in page.url:
                try:
                    page.click("text=English")
                    page.wait_for_timeout(1000)
                except:
                    pass  # Already redirected

            page.wait_for_load_state("networkidle")

            if "There are currently no outages in this district" in page.content():
                outages = 0
                customers = 0
            else:
                try:
                    rows = page.locator("table tr").all()
                    outages = len(rows) - 1  # Subtract header
                    customers = 0
                    for row in rows[1:]:
                        cells = row.locator("td").all()
                        if len(cells) >= 6:
                            cust_text = cells[5].inner_text().strip().replace(",", "")
                            customers += int(cust_text)
                except Exception as e:
                    outages = 0
                    customers = 0

            results.append({
                "region": name,
                "outages": outages,
                "customers_affected": customers
            })

        browser.close()

    with open("outages.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    scrape()
