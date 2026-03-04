"""
Simple example plugin that "asimila" (simulates) another bot's output by transforming input text.
Add more plugins here. Plugins should expose a `name` and a `process(text)` function.
"""

name = 'perchance_sample'

def process(text: str) -> str:
    # Very simple deterministic transformation to simulate a cloned capability.
    # Replace this with more advanced local processing or open-source LLM calls.
    if not text:
        return 'Nada que procesar.'
    # Example: echo with a tag and a reversed phrase
    reversed_text = text[::-1]
    return f"[PerchanceSim] Original: {text} | Reversed: {reversed_text}"
