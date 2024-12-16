from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Flask app
app = Flask(__name__)

# Telegram bot token
BOT_TOKEN = "7545746171:AAFsI8zRnrs0_INPxO6eFrCHKkukAs9FRmM"

# Telegram bot application
application = Application.builder().token(BOT_TOKEN).build()

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user  # Get the user's info
    username = user.username or user.first_name  # Fallback to first name if no username
    
    # 1. Send welcome message with a welcome image
    welcome_photo_url = "https://imgur.com/aDHfR5m"  # Replace with your welcome image URL
    welcome_caption = f"👋 Welcome to BLDX TON Miner App, {username}! 🚀\nLet's get started on your mining journey."
    await update.message.reply_photo(photo=welcome_photo_url, caption=welcome_caption)
    
    # 2. Wait for a few seconds
    await asyncio.sleep(3)  # Delay for 3 seconds
    
    # 3. Send the main miner message with buttons
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
    
    # Send the miner message with buttons
    await update.message.reply_photo(photo=miner_photo_url, caption=miner_caption, reply_markup=reply_markup)

# Add handlers to the application
application.add_handler(CommandHandler("start", start))

# Webhook route
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    """Handle incoming Telegram updates."""
    data = request.get_json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return "OK", 200

# Set webhook
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    webhook_url = f"https://afasc-pz2jycd9a-admobolokos-projects.vercel.app/{BOT_TOKEN}"  # Replace with your Vercel URL
    application.bot.set_webhook(url=webhook_url)
    return "Webhook set successfully!", 200
