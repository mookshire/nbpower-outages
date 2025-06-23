import asyncio import json from playwright.async_api import async_playwright

REGIONS = [ ("York", "0110"), ("K.V.", "0210"), ("Carleton", "0130"), ("Charlotte", "0240"), ("Kings", "0220"), ("Kent", "0510"), ("Moncton", "0520"), ("Miramichi", "0310"), ("Grand Falls", "0410"), ("Acadian", "0320"), ("Heat (Chaleur)", "0330"), ("Restigouche", "0420"), ("Sackville", "0530"), ("Shediac", "0540") ]

async def fetch_region_data(playwright, name, code): url = f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={code}&il=0" print(f"\n▶ Visiting {name} district {code}") browser = await playwright.chromium.launch(headless=False, slow_mo=500) context = await browser.new_context() page = await context.new_page()

try:
    await page.goto(url, timeout=60000)
    print("[INFO] Page loaded. Dumping HTML:")
    print(await page.content())

    await page.wait_for_selector("#ctl00_cphMain_lblOutageCount", timeout=15000)
    outages = await page.inner_text("#ctl00_cphMain_lblOutageCount")
    customers = await page.inner_text("#ctl00_cphMain_lblCustAffected")

    print(f"✔ {name}: {outages} outages, {customers} customers affected")
    await context.close()
    await browser.close()

    return {
        "region": name,
        "outages": int(outages.replace(',', '')),
        "customers_affected": int(customers.replace(',', ''))
    }

except Exception as e:
    print(f"❌ {name} FAILED: {str(e)}")
    await context.close()
    await browser.close()
    return {
        "region": name,
        "outages": -1,
        "customers_affected": -1
    }

async def main(): async with async_playwright() as playwright: results = [] for name, code in REGIONS: data = await fetch_region_data(playwright, name, code) results.append(data)

with open("outages.json", "w") as f:
        json.dump(results, f, indent=2)

if name == "main": asyncio.run(main())

