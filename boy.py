from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Initialize Flask app
app = Flask(__name__)

# Telegram bot token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Create Telegram bot application
application = Application.builder().token(TOKEN).build()


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username or user.first_name

    # Welcome message
    welcome_photo_url = "https://imgur.com/aDHfR5m"  # Replace with your welcome image URL
    welcome_caption = f"👋 Welcome to BLDX TON Miner App, {username}! 🚀\nLet's get started on your mining journey."
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=welcome_photo_url, caption=welcome_caption)

    # Miner message with buttons
    miner_photo_url = "https://imgur.com/a/6JUmXY9"  # Replace with your miner image URL
    miner_caption = (
        "Get Ready, Get Set, Mine TON! 🚀⛏️💰\n"
        "Start your journey with **BLDX TON Miner** and unlock exciting rewards! 🚀"
    )
    keyboard = [
        [InlineKeyboardButton("Open BLDX Miner", url="https://t.me/BOLDXOfficial_Bot?ref=zikky")],
        [InlineKeyboardButton("Join Community", url="https://t.me/bldxtonminers")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=miner_photo_url, caption=miner_caption, reply_markup=reply_markup)


# Add the command handler
application.add_handler(CommandHandler("start", start))


# Flask route to handle Telegram webhooks
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    # Process the incoming Telegram update
    update = Update.de_json(request.get_json(), application.bot)
    application.update_queue.put_nowait(update)
    return "OK", 200


# Flask route to set the webhook (run this once)
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    webhook_url = f"https://<your-server-domain>/{TOKEN}"  # Replace <your-server-domain> with your domain
    application.bot.set_webhook(webhook_url)
    return f"Webhook set to {webhook_url}", 200


# Flask route to clear the webhook
@app.route("/clear_webhook", methods=["GET"])
def clear_webhook():
    application.bot.delete_webhook()
    return "Webhook cleared", 200


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
