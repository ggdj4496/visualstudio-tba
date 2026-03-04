# ALPHA_BOT Project History and Backup Notes

This document records the chronological steps taken while creating and
expanding the ALPHA_BOT project. It can be used as a backup of the process of
writing files, adding folders, and developing the source code.

The history below includes the initial scaffold, new features, and structural
changes. It can help you retrace development decisions or replicate the setup
elsewhere.

---

## Initial Scaffold (early March 2026)

1. Created directory `ALPHA_BOT/`.
2. Added minimal `README.md` describing purpose and quick start.
3. Added `requirements.txt` with basic dependencies (`pytelegrambotapi`,
   `python-dotenv`).
4. Created `.env.example` with placeholder variables.
5. Wrote `utils.py` to load environment variables, configure logging, and
   provide `is_owner()` helper.
6. Added `plugins/` subdirectory and an example plugin
   `perchance_sample.py` showing simple text transformation.
7. Developed `main.py`:
   - Implemented `motor`-style polling.
   - Added start handler, message handler, and plugin keyboard.
   - Implemented simple session state for plugin selection.
   - Error handling, reload mechanism, and logging.
8. Added `smoke_test.py` to verify plugin loading.

## Enhancements

9. Expanded `requirements.txt` with utilities (`Pillow`, `requests`) and
   documented optional local LLM packages.
10. Upgraded `main.py` with additional menu options:
    - Settings (`⚙️ Ajustes`), console (`🖥️ Consola`), image processing
      (`📸 Fotox`), restart functionality.
    - Added session handling for console commands and photo uploads.
    - Implemented `safe_restart()` to re-launch the script.
11. Added `install.ps1` and `install.sh` to automate environment setup.
12. Added `PROJECT_HISTORY.md` (this file) and enhanced `README.md` with
    full explanation of features and usage.
13. Created persistent memory plugin (`plugins/memory.py`) allowing the bot to
    remember text between sessions.  Updated documentation accordingly.
14. Wrote instructions for running ALPHA as a permanent agent/service (see
    README).

## Backup & Versioning

- All file modifications are recorded here and archived via Git if
  applicable. To back up the project, simply copy the entire `ALPHA_BOT`
  directory or create a zip/tar archive:

  ```powershell
  Compress-Archive -Path ALPHA_BOT -DestinationPath ALPHA_BOT_backup.zip
  ```

  ```bash
  tar -czf ALPHA_BOT_backup.tar.gz ALPHA_BOT/
  ```

- Keeping this `PROJECT_HISTORY.md` alongside the source code ensures the
  writing process is documented even if Git metadata is unavailable.

---

Feel free to append new entries as features are added or modifications made.