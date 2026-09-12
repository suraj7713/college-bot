import json
import os
from datetime import time
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

IST = ZoneInfo("Asia/Kolkata")

SUBSCRIBERS_FILE = "subscribers.json"
DAY_FILE = "day.txt"

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


def load_subscribers():
    if not os.path.exists(SUBSCRIBERS_FILE):
        return []

    with open(SUBSCRIBERS_FILE, "r") as f:
        return json.load(f)


def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(subscribers, f)


def get_day():
    if not os.path.exists(DAY_FILE):
        with open(DAY_FILE, "w") as f:
            f.write("0")
        return 0

    with open(DAY_FILE, "r") as f:
        return int(f.read())


def save_day(day):
    with open(DAY_FILE, "w") as f:
        f.write(str(day))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    subscribers = load_subscribers()

    if chat_id not in subscribers:
        subscribers.append(chat_id)
        save_subscribers(subscribers)

    await update.message.reply_text(
        "✅ You are subscribed!\n\n"
        "Every day at 5:00 AM IST, I will send you "
        "one engineering college photo. 🏛️📸"
    )


async def test_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("photos/iit_bombay.jpg", "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="🏛️ IIT Bombay\n📍 Mumbai, Maharashtra"
            )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Photo error:\n{e}"
        )


async def send_daily_college(context: ContextTypes.DEFAULT_TYPE):
    subscribers = load_subscribers()

    if not subscribers:
        return

    day = get_day()
    college = colleges[day % len(colleges)]

    caption = (
        f"🏛️ {college['name']}\n"
        f"📍 {college['location']}\n\n"
        f"🎓 Engineering College of the Day"
    )

    for chat_id in subscribers:
        try:
            with open(college["photo"], "rb") as photo:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption
                )

        except Exception as e:
            print(f"Could not send to {chat_id}: {e}")

    save_day((day + 1) % len(colleges))


def main():
    application = Application.builder().token(TOKEN).build()

    # Telegram commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("test", test_photo))

    # Daily 5 AM IST message
    application.job_queue.run_daily(
        send_daily_college,
        time=time(hour=5, minute=0, tzinfo=IST)
    )

    print("🤖 Bot is running...")
    print("⏰ Daily college photo scheduled for 5:00 AM IST")

    application.run_polling()


if __name__ == "__main__":
    main()