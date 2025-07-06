import os
import json
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# دریافت توکن از Environment
TOKEN = os.environ.get("TOKEN")
OWNER_ID = 262011432

TEAMS_FILE = 'teams.json'
ADMINS_FILE = 'admins.json'

app = Flask(__name__)

@app.route('/')
def home():
    return "ربات فعال است!"

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_admin(user_id):
    admins = load_data(ADMINS_FILE).get("admins", [])
    return user_id == OWNER_ID or user_id in admins

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! به ربات پیش‌بینی خوش آمدید ⚽️")

async def addteam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("شما دسترسی ندارید.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("استفاده صحیح: /addteam نام_تیم")
        return
    team = context.args[0]
    data = load_data(TEAMS_FILE)
    if team in data:
        await update.message.reply_text("این تیم قبلاً اضافه شده است.")
    else:
        data[team] = {"players": []}
        save_data(TEAMS_FILE, data)
        await update.message.reply_text(f"تیم {team} اضافه شد.")

async def teams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data(TEAMS_FILE)
    if data:
        msg = "\n".join(data.keys())
        await update.message.reply_text("لیست تیم‌ها:\n" + msg)
    else:
        await update.message.reply_text("هنوز تیمی اضافه نشده است.")

def run_bot():
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CommandHandler("addteam", addteam))
    app_telegram.add_handler(CommandHandler("teams", teams))
    app_telegram.run_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)