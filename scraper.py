import aiohttp

async def fetch(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=20) as r:
                return await r.text()
    except:
        return ""


def extract_state(html):
    # lightweight detection (بدون BeautifulSoup ثقيل)
    return str(len(html))
