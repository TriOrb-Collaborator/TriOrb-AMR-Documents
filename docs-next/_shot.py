"""Visual check for 58-package umbrella build."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = "http://localhost:18100"
OUT = Path(__file__).parent / "_shots"
OUT.mkdir(exist_ok=True)

PAGES = [
    ("home", "/"),
    ("pkg_api_index", "/packages/index.html"),
    ("plc_pkg", "/packages/triorb_sick_plc_wrapper/index.html"),
    ("plc_msg", "/packages/triorb_sick_plc_wrapper/interfaces/msg/AppDataFromPLC.html"),
    ("plc_cpp", "/packages/triorb_sick_plc_wrapper/generated/class__Node.html"),
    ("battery", "/packages/triorb_battery_info/index.html"),
    ("snr_mux", "/packages/triorb_snr_mux_driver/index.html"),
    ("navigation_manager", "/packages/triorb_navigation_manager/index.html"),
    ("gamepad", "/packages/triorb_gamepad/index.html"),
    ("camera_argus", "/packages/triorb_camera_argus/index.html"),
    ("drive_interface", "/packages/triorb_drive_interface/index.html"),
    ("plc_interface", "/packages/triorb_plc_interface/index.html"),
    ("visual_slam", "/packages/visual_slam.html"),
]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await ctx.new_page()
        for name, path in PAGES:
            try:
                resp = await page.goto(BASE + path, wait_until="networkidle", timeout=20000)
                await page.screenshot(path=OUT / f"{name}.png", full_page=True)
                print(f"{name:20s} | {resp.status} | {await page.title()}")
            except Exception as e:
                print(f"{name:20s} | ERROR: {e}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
