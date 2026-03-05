from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from utils import process_alpha

TOKEN = '8528431478:AAH-Naudhhz_ExampleToken'

async def go(u, c):
    f = await u.message.photo[-1].get_file()
    i, o = f"ai_in_{f.file_id}.jpg", f"ai_out_{f.file_id}.svg"
    await f.download_to_drive(i)
    process_alpha(i, o)
    await u.message.reply_document(open(o, 'rb'))

if __name__ == '__main__':
    ApplicationBuilder().token(TOKEN).build().add_handler(MessageHandler(filters.PHOTO, go)).run_polling()
