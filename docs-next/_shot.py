"""JA translation verification."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = "http://localhost:18101"  # JA
OUT = Path(__file__).parent / "_shots"
OUT.mkdir(exist_ok=True)

PAGES = [
    ("ja_home", "/"),
    ("ja_pkg_index", "/packages/index.html"),
    ("ja_visual_slam", "/packages/visual_slam.html"),
    ("ja_plc_cpp", "/packages/triorb_sick_plc_wrapper/generated/struct__Node_1_1PubApplicationData.html"),
    ("ja_plc_msg", "/packages/triorb_sick_plc_wrapper/interfaces/msg/AppDataFromPLC.html"),
    ("ja_terms", "/guides/terms.html"),
    ("ja_privacy", "/guides/privacy.html"),
    ("ja_overview", "/guides/overview.html"),
]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await ctx.new_page()
        for name, path in PAGES:
            try:
                resp = await page.goto(BASE + path, wait_until="networkidle", timeout=30000)
                await page.screenshot(path=OUT / f"{name}.png", full_page=True)
                print(f"{name:20s} | {resp.status} | {await page.title()}")
            except Exception as e:
                print(f"{name:20s} | ERROR: {e}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
