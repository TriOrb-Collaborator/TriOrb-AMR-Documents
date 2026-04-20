"""Visual check after categorization."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = "http://localhost:18100"
OUT = Path(__file__).parent / "_shots"
OUT.mkdir(exist_ok=True)

PAGES = [
    ("pkg_api_grouped", "/packages/index.html"),
    ("home", "/"),
]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await ctx.new_page()
        for name, path in PAGES:
            resp = await page.goto(BASE + path, wait_until="networkidle", timeout=20000)
            await page.screenshot(path=OUT / f"{name}.png", full_page=True)
            print(f"{name:20s} | {resp.status} | {await page.title()}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
