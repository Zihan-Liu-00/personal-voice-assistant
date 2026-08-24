from __future__ import annotations
import asyncio, urllib.parse
from browser_use import BrowserProfile, BrowserSession

async def _search(query):
    browser=BrowserSession(browser_profile=BrowserProfile(headless=False,keep_alive=True,enable_default_extensions=False))
    try:
        await browser.start(); page=await browser.get_current_page()
        await page.goto('https://www.google.com/search?q='+urllib.parse.quote_plus(query))
        await asyncio.sleep(2)
        text=await page.evaluate('''() => document.body.innerText''')
        return text[:12000]
    finally:
        await browser.stop()

def google_search(query): return asyncio.run(_search(query))
