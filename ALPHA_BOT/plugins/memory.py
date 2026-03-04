"""
Simple persistent memory plugin. It stores each text message you send while the
plugin is active into a local file (`memory.json`) and can return the stored
history or clear it. This makes ALPHA behave like an agent with a record of
the conversation across restarts.

Usage:
- Select the plugin via the menu ("PLUGIN:memory").
- Send any text to have it appended to memory.
- Send the command `!show` to display stored memory.
- Send `!clear` to wipe the memory file.

The memory file is stored in the bot directory and is human-readable JSON.
"""

name = 'memory'

import pathlib
import json

MEM_FILE = pathlib.Path(__file__).parent.parent / 'memory.json'


def load_memory():
    if MEM_FILE.exists():
        try:
            return json.loads(MEM_FILE.read_text('utf-8'))
        except Exception:
            return []
    return []


def save_memory(records):
    MEM_FILE.write_text(json.dumps(records, ensure_ascii=False, indent=2), 'utf-8')


def process(text: str) -> str:
    if not text:
        return 'Nada que guardar.'
    if text.strip().lower() == '!show':
        mem = load_memory()
        if not mem:
            return 'La memoria está vacía.'
        return 'Registro:\n' + '\n'.join(mem)
    if text.strip().lower() == '!clear':
        save_memory([])
        return 'Memoria borrada.'
    # Append to memory
    mem = load_memory()
    mem.append(text)
    save_memory(mem)
    return f'Guardado en memoria ({len(mem)} entradas).'
