#!/bin/env python3
#
# source ~/source_me
#

import os,sys
import asyncio
import httpx
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ====== CONFIG ======
if not "MY_TELEGRAM_BOT_TOKEN" in os.environ:
    print ("Please set your Telegram bot token using the 'MY_TELEGRAM_BOT_TOKEN' environment variable.")
    sys.exit()

TELEGRAM_BOT_TOKEN = os.environ["MY_TELEGRAM_BOT_TOKEN"]
OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma3"
# ====================


async def query_ollama(prompt: str) -> str:
    """Send request to Ollama"""
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(
            OLLAMA_API_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [ {"role": "user", "content": prompt} ],
                "stream": False
            }
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Start typing indicator
    async def keep_typing():
        while True:
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=ChatAction.TYPING,
            )
            await asyncio.sleep(4)

    typing_task = asyncio.create_task(keep_typing())

    try:
        # Query Ollama
        reply = await query_ollama(user_message)

        # Send response
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

    finally:
        typing_task.cancel()


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
