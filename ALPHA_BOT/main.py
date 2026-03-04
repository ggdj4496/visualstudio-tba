import os
import sys
import logging
from telebot import TeleBot, types
from utils import TELEGRAM_TOKEN, is_owner, logger

# Dynamic plugin loader
from importlib import import_module
from glob import glob
import pathlib

PLUGINS = {}
SESSIONS = {}
DEBUG_MODE = False


def load_plugins():
    PLUGINS.clear()
    plugin_files = glob(str(pathlib.Path(__file__).parent / 'plugins' / '*.py'))
    for p in plugin_files:
        name = pathlib.Path(p).stem
        if name.startswith('_'):
            continue
        try:
            mod = import_module(f'plugins.{name}')
            if hasattr(mod, 'process') and hasattr(mod, 'name'):
                PLUGINS[mod.name] = mod
                logger.info(f'Loaded plugin: {mod.name}')
            else:
                logger.info(f'Skipped plugin (missing interface): {name}')
        except Exception as e:
            logger.exception(f'Failed to load plugin {name}: {e}')


def safe_restart():
    logger.info('Performing safe restart...')
    python = sys.executable
    os.execv(python, [python] + sys.argv)


def start_bot():
    if not TELEGRAM_TOKEN:
        logger.error('No TELEGRAM_TOKEN; aborting bot startup.')
        return

    bot = TeleBot(TELEGRAM_TOKEN)

    @bot.message_handler(commands=['start'])
    def send_welcome(m):
        if not is_owner(m.from_user.id):
            return
        markup = types.ReplyKeyboardMarkup(True, row_width=2)
        markup.add('🎨 Perchance', '📸 Fotox', '💎 Saldo: 1653 CR')
        # additional control buttons
        markup.add('⚙️ Ajustes', '🧠 Asimilar', '🖥️ Consola', '🔁 Reiniciar')
        bot.send_message(m.chat.id, f'🔱 ALPHA CONECTADO', reply_markup=markup)

    @bot.message_handler(func=lambda m: True, content_types=['text', 'photo'])
    def handle_message(m):
        if not is_owner(m.from_user.id):
            return
        text = (m.text or '').strip()
        logger.info(f'Received from owner: {text or "<photo>"}')

        if text == '🎨 Perchance':
            bot.send_message(m.chat.id, 'Selecciona un plugin para ejecutar:', reply_markup=plugin_keyboard())
            return

        if text == '⚙️ Ajustes':
            send_settings(m)
            return

        if text == '🖥️ Consola':
            bot.send_message(m.chat.id, 'Consola segura: envía `status`, `plugins`, `reload` o `help`.')
            SESSIONS[m.chat.id] = 'CONSOLE'
            return

        if text == '🧠 Asimilar':
            bot.send_message(m.chat.id, 'Asimilar: selecciona plugin o envía texto para que te devuelva la lista.', reply_markup=plugin_keyboard())
            return

        if text == '🔁 Reiniciar':
            bot.send_message(m.chat.id, 'Reiniciando...')
            safe_restart()
            return

        if text == '📸 Fotox':
            bot.send_message(m.chat.id, 'Envíame una foto para procesar.')
            SESSIONS[m.chat.id] = 'FOTO'
            return

        # Console session
        if SESSIONS.get(m.chat.id) == 'CONSOLE':
            handle_console(m, text)
            return

        # Foto session
        if SESSIONS.get(m.chat.id) == 'FOTO':
            SESSIONS.pop(m.chat.id, None)
            if m.content_type == 'photo' or hasattr(m, 'photo'):
                try:
                    file_info = bot.get_file(m.photo[-1].file_id)
                    downloaded = bot.download_file(file_info.file_path)
                    from io import BytesIO
                    from PIL import Image, ImageOps
                    img = Image.open(BytesIO(downloaded))
                    img = ImageOps.grayscale(img)
                    out = BytesIO()
                    img.save(out, format='PNG')
                    out.seek(0)
                    bot.send_photo(m.chat.id, out, caption='Foto procesada: escala de grises')
                except Exception as e:
                    logger.exception('Error procesando foto')
                    bot.send_message(m.chat.id, f'Error procesando foto: {e}')
            else:
                bot.send_message(m.chat.id, 'No recibí una foto.')
            return

        # Plugin selection by special message
        if text.startswith('PLUGIN:'):
            plugin_key = text.split(':', 1)[1].strip()
            plugin = PLUGINS.get(plugin_key)
            if not plugin:
                bot.send_message(m.chat.id, f'Plugin {plugin_key} no encontrado.')
                return
            bot.send_message(m.chat.id, 'Envíame el texto a asimilar (responderé con el resultado procesado).')
            SESSIONS[m.chat.id] = plugin_key
            return

        # If session expects a plugin, process
        if SESSIONS.get(m.chat.id):
            current = SESSIONS.pop(m.chat.id)
            if current in PLUGINS:
                plugin = PLUGINS.get(current)
                try:
                    result = plugin.process(text)
                except Exception as e:
                    result = f'Error en plugin: {e}'
                bot.send_message(m.chat.id, result)
                return

        # Fallback echo
        bot.reply_to(m, f'ALPHA recibió: {text or "<non-text>"}')

    def plugin_keyboard():
        kb = types.ReplyKeyboardMarkup(True, row_width=2)
        for k in PLUGINS.keys():
            kb.add(f'PLUGIN:{k}')
        kb.add('🔙 Volver')
        return kb

    def send_settings(m):
        kb = types.ReplyKeyboardMarkup(True, row_width=2)
        kb.add(f'DEBUG: {str(DEBUG_MODE)}', 'Reload Plugins', 'Show Owner')
        bot.send_message(m.chat.id, 'Ajustes:', reply_markup=kb)

    def handle_console(m, text):
        cmd = (text or '').lower()
        if cmd == 'status':
            bot.send_message(m.chat.id, f'Plugins loaded: {len(PLUGINS)}')
            return
        if cmd == 'plugins':
            bot.send_message(m.chat.id, 'Plugins: ' + ', '.join(PLUGINS.keys() or ['(none)']))
            return
        if cmd == 'reload':
            load_plugins()
            bot.send_message(m.chat.id, 'Plugins recargados.')
            return
        if cmd == 'help':
            bot.send_message(m.chat.id, 'Consola comandos: status, plugins, reload, help')
            return
        bot.send_message(m.chat.id, 'Comando no reconocido. Envía `help` para ver comandos.')

    load_plugins()

    logger.info('ALPHA bot starting polling...')
    try:
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except Exception as e:
        logger.exception(f'Bot polling stopped: {e}')


if __name__ == '__main__':
    start_bot()
