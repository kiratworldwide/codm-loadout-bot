import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
from flask import Flask  # NEW: Import Flask
from threading import Thread  # NEW: For running Flask in background

# ===== FLASK KEEP-ALIVE SERVER ===== # NEW SECTION
app = Flask(__name__)

@app.route('/')
def home():
    return "CODM Loadout Bot is running! ✅"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# === Load guns from JSON === 
with open('guns.json', 'r') as f:
    guns = json.load(f)

# === Logging ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Welcome to CODM Loadout Guru!\n\n"
        "Use /loadout [gun_name] to get the best meta build.\n"
        "Example: /loadout m4"
    )

async def loadout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Please specify a gun name.\nExample: /loadout m4"
        )
        return

    gun_name = " ".join(context.args).lower()
    data = guns.get(gun_name)

    if data:
        reply = f"🔫 **{gun_name.upper()} META LOADOUT:**\n\n"
        reply += "\n".join([f"- {a}" for a in data['attachments']])
        reply += f"\n\n💡 **Tip:** {data['tip']}"
        await update.message.reply_text(reply, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "😢 Sorry, I don't have that gun yet.\n"
            "Try another name!\n"
            "Example: /loadout m4 or /loadout ak-47"
        )

# === Run Bot ===
def main():
    TOKEN = "8104047362:AAE6kmylRLeSH4QQr_iqKBYb6ATmOrXXWSc"  # ⚠️ Replace with your token
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("loadout", loadout))

    # ===== START FLASK IN BACKGROUND ===== # NEW
    Thread(target=run_flask).start()  # Replaces keep_alive.py

    application.run_polling()

if __name__ == '__main__':
    main()