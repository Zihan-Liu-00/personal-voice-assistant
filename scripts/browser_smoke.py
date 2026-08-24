import asyncio
from browser_use import BrowserProfile, BrowserSession

async def main():
    profile=BrowserProfile(headless=False,keep_alive=True,enable_default_extensions=False,disable_security=False)
    browser=BrowserSession(browser_profile=profile)
    await browser.start()
    print('BROWSER_STARTED', flush=True)
    await browser.navigate_to('https://www.google.com')
    print('BROWSER_CONNECTED_GOOGLE', flush=True)
    page=await browser.get_current_page()
    print('PAGE_METHODS', [x for x in dir(page) if x in ('goto','evaluate','content','get_content','locator','get_by_role','get_by_text')], flush=True)
    await asyncio.sleep(5)
    await browser.stop()

asyncio.run(main())
