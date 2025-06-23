import asyncio import json from playwright.async_api import async_playwright

REGIONS = [ ("York", "0110"), ("K.V.", "0210"), ("Carleton", "0130"), ("Charlotte", "0240"), ("Kings", "0220"), ("Kent", "0510"), ("Moncton", "0520"), ("Miramichi", "0420"), ("Grand Falls", "0140"), ("Acadian", "0440"), ("Heat", "0410"), ("Restigouche", "0430"), ("Sackville", "0530"), ("Shediac", "0540") ]

async def scrape(): results = [] async with async_playwright() as p: browser = await p.chromium.launch(headless=True) context = await browser.new_context()

for region_name, district_code in REGIONS:
        page = await context.new_page()

        try:
            url = f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={district_code}&il=0"
            await page.goto(url, timeout=30000)
            await page.wait_for_selector("#ctl00_cphMain_lblOutageCount", timeout=10000)
            outages = await page.locator("#ctl00_cphMain_lblOutageCount").inner_text()
            customers = await page.locator("#ctl00_cphMain_lblCustAffectedCount").inner_text()

            results.append({
                "region": region_name,
                "outages": int(outages.strip()),
                "customers_affected": int(customers.strip())
            })
        except Exception as e:
            print(f"⚠️ {region_name} FAILED: {e}")
            results.append({
                "region": region_name,
                "outages": -1,
                "customers_affected": -1
            })
        finally:
            await page.close()

    await browser.close()

with open("outages.json", "w") as f:
    json.dump(results, f, indent=2)

print(">>> SCRAPE COMPLETE")

if name == "main": asyncio.run(scrape())

