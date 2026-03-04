import cv2
import numpy as np
import os

def start(bot, m):
    msg = bot.send_message(m.chat.id, "☣️ **RASTREO DE PIXELES**\nEnvia la FOTO ORIGINAL.")
    bot.register_next_step_handler(msg, get_orig, bot)

def get_orig(m, bot):
    if not m.photo: return
    info = bot.get_file(m.photo[-1].file_id)
    with open('logs/orig.jpg', 'wb') as f: f.write(bot.download_file(info.file_path))
    msg = bot.send_message(m.chat.id, "✅ Recibida. Envia el RESULTADO del bot donante.")
    bot.register_next_step_handler(msg, compare, bot)

def compare(m, bot):
    if not m.photo: return
    info = bot.get_file(m.photo[-1].file_id)
    with open('logs/res.jpg', 'wb') as f: f.write(bot.download_file(info.file_path))
    bot.send_message(m.chat.id, "🧬 Analizando variaciones de color y estructura...")
    
    img1 = cv2.imread('logs/orig.jpg')
    img2 = cv2.imread('logs/res.jpg')
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    
    # Diferencia absoluta para ver que pixeles cambio el bot
    diff = cv2.absdiff(img1, img2)
    cv2.imwrite('logs/mapa_sigma.jpg', diff)
    
    with open('logs/mapa_sigma.jpg', 'rb') as f:
        bot.send_photo(m.chat.id, f, caption="📊 MAPA DE ASIMILACION\nLo brillante es lo que el bot original modifico.")