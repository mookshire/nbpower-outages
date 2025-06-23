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
        await page.goto(url, timeout=20000)
        # Wait for the outage and customer labels to load
        await page.wait_for_selector("#ctl00_cphMain_lblOutageCount", timeout=10000)
        await page
