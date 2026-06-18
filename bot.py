import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import BOT_TOKEN, CHECK_INTERVAL
from db import add_track, get_tracks, update_track
from scraper import fetch, extract_state

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

user_state = {}

# ---------------- START ----------------
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🚀 Lite Tracker Bot Ready\n\n"
        "/track URL - add link\n"
        "/my - show links"
    )


# ---------------- ADD TRACK ----------------
@dp.message(Command("track"))
async def track(message: types.Message):

    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        return await message.answer("❌ Use: /track URL")

    url = parts[1]
    add_track(message.from_user.id, url)

    await message.answer("✅ Added")


# ---------------- SHOW ----------------
@dp.message(Command("my"))
async def my(message: types.Message):

    data = get_tracks()
    uid = message.from_user.id

    links = [t for t in data if t[1] == uid]

    if not links:
        return await message.answer("❌ No tracks")

    text = "📚 Your links:\n\n"

    for i, t in enumerate(links, 1):
        text += f"{i}. {t[2]}\n"

    await message.answer(text)


# ---------------- SAFE WATCHER ----------------
async def watcher():

    while True:

        tracks = get_tracks()

        for t in tracks:

            tid, uid, url, old = t

            html = await fetch(url)

            if not html:
                continue

            new = extract_state(html)

            if old and old != new:
                try:
                    await bot.send_message(
                        uid,
                        f"📢 Update detected\n{url}"
                    )
                except:
                    pass

            update_track(tid, new)

        await asyncio.sleep(CHECK_INTERVAL)


# ---------------- MAIN ----------------
async def main():
    print("BOT RUNNING 🚀")

    asyncio.create_task(watcher())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
