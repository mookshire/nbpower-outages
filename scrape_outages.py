import asyncio
import json
from playwright.async_api import async_playwright

REGIONS = [
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

async def fetch_region_data(playwright, name, district_code):
    browser = await playwright.chromium.launch()
    page = await browser.new_page()
    url = f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={district_code}&il=0"

    try:
        print(f"▶ Visiting {name} district {district_code}")
        await page.context.add_cookies([{
            'name': 'NBPLanguage',
            'value': 'en',
            'domain': 'www.nbpower.com',
            'path': '/',
            'httpOnly': False,
            'secure': True
        }])

        await page.goto(url, timeout=30000)
        await page.wait_for_selector("#ctl00_cphMain_lblOutageCount", timeout=15000)
        await page.wait_for_selector("#ctl00_cphMain_lblCustomersAffected", timeout=15000)

        outages = await page.locator("#ctl00_cphMain_lblOutageCount").inner_text()
        customers = await page.locator("#ctl00_cphMain_lblCustomersAffected").inner_text()

        print(f"✅ {name}: {outages} outages, {customers} customers affected")

        return {
            "region": name,
            "outages": int(outages.replace(",", "").strip()),
            "customers_affected": int(customers.replace(",", "").strip())
        }

    except Exception as e:
        print(f"❌ {name} FAILED: {e}")
        await page.screenshot(path=f"{name.lower().replace(' ', '_')}.png")
        return {
            "region": name,
            "outages": -1,
            "customers_affected": -1
        }

    finally:
        await browser.close()

async def main():
    async with async_playwright() as playwright:
        results = []
        for name, code in REGIONS:
            data = await fetch_region_data(playwright, name, code)
            results.append(data)

        with open("outages.json", "w") as f:
            json.dump(results, f, indent=2)
        print("💾 Saved to outages.json")

if __name__ == "__main__":
    asyncio.run(main())
