import asyncio import json from playwright.async_api import async_playwright

Define region names and corresponding NB Power district codes

REGIONS = [ ("York", "0110"), ("K.V.", "0210"), ("Carleton", "0130"), ("Charlotte", "0240"), ("Kings", "0220"), ("Kent", "0510"), ("Moncton", "0520"), ("Miramichi", "0420"), ("Grand Falls", "0140"), ("Acadian", "0440"), ("Heat", "0410"), ("Restigouche", "0430"), ("Sackville", "0530"), ("Shediac", "0540"), ]

async def scrape(): async with async_playwright() as p: browser = await p.chromium.launch(headless=True) context = await browser.new_context()

# Bypass language selector by setting language preference cookie
    await context.add_cookies([{
        "name": "NBPLanguage",
        "value": "en-CA",
        "domain": "www.nbpower.com",
        "path": "/",
        "httpOnly": False,
        "secure": True
    }])

    page = await context.new_page()
    result = []

    for region_name, district_code in REGIONS:
        url = f"https://www.nbpower.com/Open/SearchOutageResults.aspx?district={district_code}&il=0"
        print(f"→ {region_name}: Visiting {url}")

        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_selector("#ctl00_cphMain_lblOutageCount", timeout=10000)
            await page.wait_for_selector("#ctl00_cphMain_lblCustAffectedCount", timeout=10000)

            outages = await page.inner_text("#ctl00_cphMain_lblOutageCount")
            customers = await page.inner_text("#ctl00_cphMain_lblCustAffectedCount")

            outages = int(outages.replace(",", "").strip())
            customers = int(customers.replace(",", "").strip())
        except Exception as e:
            print(f"⚠️ {region_name} FAILED: {e}")
            outages = -1
            customers = -1

        result.append({
            "region": region_name,
            "outages": outages,
            "customers_affected": customers
        })

    await browser.close()

    with open("outages.json", "w") as f:
        json.dump(result, f, indent=2)
    print("✅ JSON written to file")

if name == "main": asyncio.run(scrape())

