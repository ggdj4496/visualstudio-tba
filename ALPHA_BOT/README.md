# ALPHA_BOT

A lightweight Telegram‑bot scaffold that runs entirely on your machine and is
extended via simple Python *plugins*.

The core idea is to **keep secrets out of code**, process input locally and let
you hook in any “asimilar” (simulate / transform / compute) logic.

---

## 🚀 Features

- **Modular plugin system** – drop new files under `plugins/` that expose a
  handler, and the bot picks them up automatically.
- **Secure configuration** – no tokens or credentials are hard‑coded.  
  They are read from the environment (or a `.env` file) and **never logged**.
- **Telegram menu navigation** – the bot exposes a simple command/menu
  structure for interacting with available plugins.
- **Lightweight & portable** – pure Python, no database required.
- Example plugins (`perchance_sample.py`, `memory.py`) illustrate how to add
  local behaviour.

---

## 🛠️ Installation & Setup

### 1. Prepare environment variables

Create a `.env` file in the root of the project by copying `.env.example`:

```bash
cp .env.example .env           # Linux/macOS
copy .env.example .env         # Windows PowerShell/Command Prompt
```

Edit `.env` and set at least:

- `TELEGRAM_TOKEN` – your bot API token from BotFather.
- `OWNER_ID` – your numeric Telegram user ID (for admin commands, etc.).

> **Note:** tokens are **never committed or stored** anywhere in the repo or
> logs. Keep your `.env` file private.

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

Ensure you have Python 3.8+ installed and that `python`/`pip` are on your path.
You may want to use a virtual environment (`venv`, `conda`, etc).

---

## ▶️ Running the Bot

```bash
python main.py
```

The bot will start polling Telegram for updates. You should see console logs
indicating it is ready.

---

### 🧠 Running as a permanent agent

To keep ALPHA running continuously, configure it as a background service or
startup task:

- **Windows:** use Task Scheduler or a tool such as [NSSM](https://nssm.cc/) to
  wrap `python main.py` in a service. You can also create a Startup shortcut to
  a script that activates the virtualenv and launches the bot.
- **Linux/macOS:** create a `systemd` service file or an `init` script that
  executes `python /path/to/ALPHA_BOT/main.py` under your virtual environment.
  Example `systemd` unit:

  ```ini
  [Unit]
  Description=ALPHA Telegram Agent
  After=network.target

  [Service]
  Type=simple
  User=youruser
  WorkingDirectory=/path/to/ALPHA_BOT
  ExecStart=/path/to/ALPHA_BOT/.venv/bin/python main.py
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```

Persisting across reboots ensures ALPHA is always available as your personal
assistant.

---

## 💬 Using the Bot

Once running, open Telegram and start a conversation with your bot.

- Send `/start` to begin; the bot will reply with a menu of available actions
  derived from loaded plugins.
- Use the inline keyboard or text commands as provided by each plugin.
- Example: in the sample plugin there may be a “perchance” option that generates
  random text.

The menu system is built into `main.py` – new plugins simply register
callbacks and the bot adds them to the keyboard.

---

## 🧩 Extending with Plugins

1. Create a new file in `plugins/`, e.g. `my_feature.py`.
2. Implement a handler function like the examples below:
   ```python
   name = 'my_feature'
   def process(text: str) -> str:
       # your logic here, return the response text
       return "ok"
   ```
   - Import standard libraries, perform file I/O, call an LLM, etc.
   - You can also respond to photos by modifying `main.py` if needed.
3. No registration is needed: the bot dynamically loads any module that exposes
   a `name` string and a `process()` callable. Avoid filenames beginning with
   underscore (`_`) if you don’t want them loaded.
4. The built-in `plugin_keyboard()` helper in `main.py` automatically adds each
   plugin name to the reply keyboard so you can select it with a button.

Plugins may also support commands such as `!show`, `!clear`, or any custom
protocol you design (see `plugins/memory.py` for a persistent example).

---

## ✅ Verification & Smoke Testing

A simple smoke test (`smoke_test.py`) is included to verify basic
functionality without Telegram:

```bash
python smoke_test.py
```

This script exercises core utilities and ensures the plugin loader and env
reader behave as expected.

For manual verification:

1. Start the bot (`python main.py`).
2. Send `/start` from your Telegram account (must match `OWNER_ID` if
   restricted).
3. Use any menu option; ensure replies are sensible and no sensitive data is
   returned.

Monitor console output for errors – they should not contain tokens or
credentials.

---

## 💻 Platform Notes

### Windows

- Use Command Prompt or PowerShell.
- To set up a virtual environment:
  ```powershell
  python -m venv venv
  .\\venv\\Scripts\\Activate.ps1   # PowerShell
  .\\venv\\Scripts\\activate.bat   # cmd.exe
  ```
- Install packages and run as above.

### Linux / macOS

- Use a terminal emulator.
- Virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```
- Proceed with installation and execution as shown earlier.

---

## ⚠️ Important Reminders

- **Environment variables only.** Do not paste your API token anywhere in
  code or issue trackers.
- **No token storage.** The bot reads the token at runtime and never writes it
  to disk or logs.
- **Owner‑only commands.** Respect the `OWNER_ID` setting; administrative
  features will be gated accordingly.

---

## 📁 Project Structure

```
ALPHA_BOT/
├── install.ps1
├── install.sh
├── main.py              # Bot entrypoint & menu logic
├── README.md            # ← this file
├── requirements.txt
├── smoke_test.py        # Basic self‑check script
├── utils.py             # Helper functions / env loader
├── PROJECT_HISTORY.md   # Change log and backup notes
├── memory.json          # (generated) persistent storage by memory plugin
└── plugins/
    ├── memory.py        # Persistent memory example
    ├── perchance_sample.py  # Simple transformation example
    └── __pycache__/
```

---

Feel free to fork, extend and adapt the bot for your own local automation or
testing needs. Happy hacking! 🔧🤖
