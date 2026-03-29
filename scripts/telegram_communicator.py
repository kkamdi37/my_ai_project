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
#OLLAMA_MODEL = "qwen3.5"

MAX_HISTORY = 3  # limit conversation length
# ====================

# Track running tasks per chat
active_tasks = {}

# Store conversation memory per chat
chat_histories = {}


async def query_ollama(messages):
    """Call Ollama chat API with history"""
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(
            OLLAMA_API_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]


def get_history(chat_id):
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []
    return chat_histories[chat_id]


def trim_history(history):
    """Keep only recent messages"""
    if len(history) > MAX_HISTORY * 2:
        return history[-MAX_HISTORY * 2 :]
    return history


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_message = update.message.text.strip()

    # 🔴 INTERRUPT COMMAND
    if user_message.lower() in ["stop", "/stop", "cancel"]:
        if chat_id in active_tasks:
            active_tasks[chat_id].cancel()
            del active_tasks[chat_id]
            await update.message.reply_text("⛔ Generation stopped.")
        else:
            await update.message.reply_text("Nothing to stop.")
        return

    # 🧹 RESET MEMORY
    if user_message.lower() in ["/reset", "reset"]:
        chat_histories[chat_id] = []
        await update.message.reply_text("🧠 Memory cleared.")
        return

    # Prevent overlapping requests
    if chat_id in active_tasks:
        await update.message.reply_text("⚠️ Already generating. Send 'stop' to cancel.")
        return

    history = get_history(chat_id)

    async def process():
        # Typing indicator loop
        async def keep_typing():
            while True:
                await context.bot.send_chat_action(
                    chat_id=chat_id,
                    action=ChatAction.TYPING,
                )
                await asyncio.sleep(4)

        typing_task = asyncio.create_task(keep_typing())

        try:
            # Add user message to history
            history.append({"role": "user", "content": user_message})

            # Trim history before sending
            messages = trim_history(history)

            # Query Ollama
            reply = await query_ollama(messages)

            # Save assistant response
            history.append({"role": "assistant", "content": reply})

            # Send reply
            await update.message.reply_text(reply)

        except asyncio.CancelledError:
            await update.message.reply_text("⛔ Generation interrupted.")
            raise

        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

        finally:
            typing_task.cancel()
            if chat_id in active_tasks:
                del active_tasks[chat_id]

    # Create and store task
    task = asyncio.create_task(process())
    active_tasks[chat_id] = task


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running (memory + interrupt enabled)...")
    app.run_polling()


if __name__ == "__main__":
    main()
