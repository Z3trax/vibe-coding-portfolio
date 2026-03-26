#!/usr/bin/env bash
set -euo pipefail

python3 -m PyInstaller --noconfirm --clean --onefile --windowed \
  --name "calculator+" \
  --icon "/Users/maxims/Documents/Projects/calculator+/assets/icon.png" \
  "/Users/maxims/Documents/Projects/calculator+/app.py"

echo "Готово. Приложение: /Users/maxims/Documents/Projects/calculator+/dist/calculator+.app"
