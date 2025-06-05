from pyrogram import Client, filters
#from config import API_ID, API_HASH, BOT_TOKEN
from instagram import download_instagram_post

API_ID = '3335796'
API_HASH = '138b992a0e672e8346d8439c3f42ea78'
BOT_TOKEN = '1396293494:AAE6YAY-Vog3QPvSNCo8x80FsIue9FJGWh8'

bot = Client("insta-downloader-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply("سلام! 👋\nلینک پست یا ریلز اینستاگرام رو بفرست تا برات دانلود کنم.")

@bot.on_message(filters.text & filters.private)
async def downloader_handler(client, message):
    url = message.text.strip()
    if "instagram.com" not in url:
        return await message.reply("⚠️ لطفاً یک لینک معتبر اینستاگرام بفرست.")

    await message.reply("🔍 در حال دریافت اطلاعات...")

    media_list = download_instagram_post(url)

    if not media_list:
        return await message.reply("❌ خطا در دریافت داده. دوباره امتحان کن.")

    for media in media_list:
        if media["type"] == "image":
            await message.reply_photo(media["url"])
        elif media["type"] == "video":
            await message.reply_video(media["url"])
        else:
            await message.reply(f"❓ نوع ناشناخته: {media['type']}")

bot.run()
