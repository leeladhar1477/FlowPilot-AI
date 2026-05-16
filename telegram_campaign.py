from telegram import Bot
import asyncio

# -----------------------------------
# BOT TOKEN
# -----------------------------------

TOKEN = "8930206290:AAGCdq34sOoDNPTb5Qadlk81RBjLzGDHTRg"

# -----------------------------------
# CHAT ID
# -----------------------------------

CHAT_ID = "6532543741"

# -----------------------------------
# IMAGE PATH
# -----------------------------------

IMAGE_PATH = "images/cric.jpg"

# -----------------------------------
# CAPTION
# -----------------------------------

CAPTION = """
CRICKET TOURNAMENT IS HERE!

Get ready for thrilling matches, explosive sixes, unforgettable wickets and crowd energy.

Competitive Teams | Intense Rivalries | Big Hits | Non-stop Entertainment

Don't miss the biggest cricket event of the season!
"""

# -----------------------------------
# SEND IMAGE
# -----------------------------------

async def send_image():

    bot = Bot(token=TOKEN)

    with open(IMAGE_PATH, "rb") as photo:

        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo,
            caption=CAPTION
        )

    print("Image + caption sent successfully!")

asyncio.run(send_image())