"""Basic smoke test to verify plugin loading and plugin processing without starting the bot."""
import sys
from importlib import import_module
from glob import glob
import pathlib

ROOT = pathlib.Path(__file__).parent
PLUGIN_DIR = ROOT / 'plugins'

plugins = []
for p in glob(str(PLUGIN_DIR / '*.py')):
    name = pathlib.Path(p).stem
    if name.startswith('_'):
        continue
    try:
        mod = import_module(f'plugins.{name}')
        if hasattr(mod, 'process') and hasattr(mod, 'name'):
            plugins.append((mod.name, mod))
    except Exception as e:
        print('Failed to import', name, e)

print('Discovered plugins:', [n for n,_ in plugins])

# Run a small input through each plugin
sample = 'Hola mundo'
for n, mod in plugins:
    try:
        out = mod.process(sample)
        print(f'[{n}] ->', out)
    except Exception as e:
        print(f'[{n}] raised error:', e)

print('Smoke test finished.')
