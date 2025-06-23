import asyncio
import json
from playwright.async_api import async_playwright

# Districts and their codes (in desired display order)
DISTRICTS = [
    ("York", "0110"),
    ("K.V.", "0210"),
    ("Carleton", "0130"),
    ("Charlotte", "0240"),
    ("Kings", "0220"),
    ("Kent", "0510"),
    ("Moncton", "0520"),
    ("Miramichi", "0310"),
    ("Grand Falls", "0140"),
    ("Acadian", "0410"),
    ("Heat (Chaleur)", "0420"),
    ("Restigouche", "0320"),
    ("Sackville", "0610"),
    ("Shediac", "0620")
]

# Core scraping logic
async def fetch_region_data(playwright, name, code):
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    url = f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={code}&il=0"
    print(f"▶ Visiting {name} district {code}")
    try:
        await page.goto(url, timeout=30000)
        await page.wait_for_selector("#ctl00_cphMain_lblOutageCount", timeout=15000)
        outages = await page.inner_text("#ctl00_cphMain_lblOutageCount")
        customers = await page.inner_text("#ctl00_cphMain_lblCustomerCount")
    except Exception as e:
        print(f"❌ {name} FAILED: {e}")
        outages = -1
        customers = -1
    await browser.close()
    return {
        "region": name,
        "outages": int(outages.replace(',', '')) if str(outages).isdigit() else -1,
        "customers_affected": int(customers.replace(',', '')) if str(customers).isdigit() else -1
    }

# Main orchestration
async def main():
    results = []
    async with async_playwright() as playwright:
        for name, code in DISTRICTS:
            data = await fetch_region_data(playwright, name, code)
            results.append(data)
    with open("outages.json", "w") as f:
        json.dump(results, f, indent=2)
    print("✅ Done writing outages.json")

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
