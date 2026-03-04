import os
import telebot
from telebot import types
from utils import Config, is_owner, logger
from importlib import import_module
from glob import glob

bot = telebot.TeleBot(Config.TOKEN)
PLUGINS = {}

def load_plugins():
    PLUGINS.clear()
    files = glob(os.path.join(Config.BASE_DIR, 'plugins', '*.py'))
    for f in files:
        name = os.path.basename(f)[:-3]
        if name.startswith('__'): continue
        try:
            module = import_module(f'plugins.{name}')
            PLUGINS[name] = module
            logger.info(f'Modulo {name} asimilado.')
        except Exception as e:
            logger.error(f'Error cargando {name}: {e}')

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('🚀 START', '⚙️ AJUSTES', '🧩 FUNCIONES', '🧬 FUNCIONES ASIMILADAS', '☣️ ASIMILAR')
    return markup

@bot.message_handler(func=lambda m: is_owner(m.from_user.id))
def core(m):
    if m.text in ['🚀 START', '/start']:
        bot.send_message(m.chat.id, "🔱 **GEMINI_ALPHA (SIGMA) ACTIVO**\nEntorno: C:\visualstudio tba\GEMINI_ALPHA", reply_markup=main_menu(), parse_mode='Markdown')
    elif m.text == '🧩 FUNCIONES':
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add('🎨 PERCHANCE', '📸 CLON_ORIGINAL', '⬅️ VOLVER')
        bot.send_message(m.chat.id, "Arsenal de funciones:", reply_markup=kb)
    elif m.text == '☣️ ASIMILAR':
        if 'assimilator' in PLUGINS:
            PLUGINS['assimilator'].start(bot, m)
    elif m.text == '⬅️ VOLVER':
        bot.send_message(m.chat.id, "Nucleo.", reply_markup=main_menu())

if __name__ == '__main__':
    load_plugins()
    logger.info("Unidad SIGMA en linea.")
    bot.infinity_polling()