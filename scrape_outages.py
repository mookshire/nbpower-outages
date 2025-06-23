import json
import asyncio
from playwright.async_api import async_playwright

# Your districts and their codes (custom order)
districts = [
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

async def fetch_region_data(playwright, name, code):
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()

    # Set language cookie to bypass language selector
    await context.add_cookies([{
        "name": "Language",
        "value": "en-CA",
        "domain": "www.nbpower.com",
        "path": "/",
        "httpOnly": False,
        "secure": True
    }])

    url = f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={code}&il=0"
    print(f"▶ Visiting {name} district {code}")

    try:
        await page.goto(url, wait_until="networkidle", timeout=45000)
        await page.wait_for_selector("#ctl00_cphMain_lblOutageCount", timeout=30000)
        outages = await page.inner_text("#ctl00_cphMain_lblOutageCount")
        customers = await page.inner_text("#ctl00_cphMain_lblCustomerCount")
    except Exception as e:
        print(f"❌ {name} FAILED: {e}")
        # Dump page content to debug what's going on
        content = await page.content()
        with open(f"{name.replace(' ', '_').lower()}_error.html", "w", encoding="utf-8") as f:
            f.write(content)
        outages = -1
        customers = -1
    await browser.close()
    return {
        "region": name,
        "outages": int(outages.replace(',', '')) if str(outages).replace(',', '').isdigit() else -1,
        "customers_affected": int(customers.replace(',', '')) if str(customers).replace(',', '').isdigit() else -1
    }

async def main():
    async with async_playwright() as playwright:
        results = []
        for name, code in districts:
            data = await fetch_region_data(playwright, name, code)
            results.append(data)
        with open("outages.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print("✅ Done writing outages.json")

if __name__ == "__main__":
    asyncio.run(main())
