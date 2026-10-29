import os, json, websockets
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

DERIV_TOKEN = os.getenv("DERIV_API_TOKEN")
DERIV_APP_ID = os.getenv("DERIV_APP_ID", "1089")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_ID = int(os.getenv("TELEGRAM_ALLC", "0"))

async def get_balance():
    uri = f"wss://ws.binaryws.com/websockets/v3?app_id={DERIV_APP_ID}"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"authorize": DERIV_TOKEN}))
        await ws.recv()
        await ws.send(json.dumps({"balance": 1}))
        bal = await ws.recv()
        return bal

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_ID: return
    await update.message.reply_text("✅ Empire94 Bot Active on Render!\n\n/balance - Check balance\n/start - Help")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_ID: return
    await update.message.reply_text("⏳ Checking balance...")
    try:
        result = await get_balance()
        data = json.loads(result)
        b = data.get("balance", {}).get("balance", "N/A")
        c = data.get("balance", {}).get("currency", "USD")
        await update.message.reply_text(f"💰 Balance: {b} {c}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
