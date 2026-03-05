import os, cv2, numpy as np
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from utils import process_sigma

# Credencial inyectada directamente
TOKEN = '8488348575:AAH-Ndkefh_ExampleToken' # Basado en tu lista

async def go(u, c):
    f = await u.message.photo[-1].get_file()
    i, o = f"in_{f.file_id}.jpg", f"out_{f.file_id}.svg"
    await f.download_to_drive(i)
    process_sigma(i, o)
    await u.message.reply_document(open(o, 'rb'))
    for x in [i, o]: os.remove(x) if os.path.exists(x) else None

if __name__ == '__main__':
    ApplicationBuilder().token(TOKEN).build().add_handler(MessageHandler(filters.PHOTO, go)).run_polling()
