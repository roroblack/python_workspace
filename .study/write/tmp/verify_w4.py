"""Headless verify retrospective_w4.html — image load + overflow check."""
import sys, io, asyncio
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from playwright.async_api import async_playwright

HTML = Path(r"c:\_proj\python_workspace\.blog\retrospective_w4.html").resolve().as_uri()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await ctx.new_page()
        await page.goto(HTML, wait_until="networkidle")

        # 1) image natural sizes
        imgs = await page.eval_on_selector_all("img", """
            els => els.map(e => ({
                src_prefix: e.src.slice(0, 30),
                naturalWidth: e.naturalWidth,
                naturalHeight: e.naturalHeight,
                alt: e.alt
            }))
        """)
        bad = [i for i in imgs if i["naturalWidth"] == 0]
        print(f"images total : {len(imgs)} | broken : {len(bad)}")
        for i in imgs:
            print(f"  {i['naturalWidth']:>4}x{i['naturalHeight']:<4}  {i['alt'][:40]}")

        # 2) overflow check (any element wider than its container)
        over = await page.evaluate("""
            () => {
                const out = [];
                const sel = ['pre', '.terminal-body', '.ascii', 'table', 'code'];
                document.querySelectorAll(sel.join(',')).forEach(el => {
                    if (el.scrollWidth > el.clientWidth + 1) {
                        out.push({tag: el.tagName, cls: el.className,
                                  scrollWidth: el.scrollWidth,
                                  clientWidth: el.clientWidth,
                                  textHead: (el.textContent||'').trim().slice(0,40)});
                    }
                });
                return out;
            }
        """)
        print(f"overflow elements: {len(over)}")
        for o in over[:10]:
            print(f"  {o['tag']}.{o['cls']}  {o['scrollWidth']}>{o['clientWidth']}  '{o['textHead']}'")

        # 3) body height / doc summary
        h = await page.evaluate("() => document.body.scrollHeight")
        title = await page.title()
        print(f"title: {title}")
        print(f"body scrollHeight: {h}")

        await browser.close()

asyncio.run(main())
