import os
from datetime import date
import asyncio
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

colleges = [
    {
        "name": "IIT Bombay",
        "location": "Mumbai, Maharashtra",
        "photo": "photos/iit_bombay.jpg"
    },
    {
        "name": "IIT Delhi",
        "location": "New Delhi",
        "photo": "photos/iit_delhi.jpg"
    },
    {
        "name": "IIT Madras",
        "location": "Chennai, Tamil Nadu",
        "photo": "photos/iit_madras.jpg"
    },
    {
        "name": "IIT Kanpur",
        "location": "Kanpur, Uttar Pradesh",
        "photo": "photos/iit_kanpur.jpg"
    },
    {
        "name": "IIT Kharagpur",
        "location": "Kharagpur, West Bengal",
        "photo": "photos/iit_kharagpur.jpg"
    }
]

# Changes automatically every day
day_number = (date.today() - date(2026, 9, 12)).days
college = colleges[day_number % len(colleges)]

caption = (
    f"🏛️ {college['name']}\n"
    f"📍 {college['location']}\n\n"
    f"🎓 Engineering College of the Day"
)

async def send_photo():
    bot = Bot(token=TOKEN)

    with open(college["photo"], "rb") as photo:
        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo,
            caption=caption
        )

    print(f"Sent: {college['name']}")


asyncio.run(send_photo())
