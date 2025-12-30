#!/bin/bash
# Builds the GUI app for Windows using Docker and PyInstaller
# Fixes the missing customtkinter data files issue

docker run --rm -v "$(pwd):/src/" --entrypoint /bin/sh cdrx/pyinstaller-windows -c "python -m pip install --upgrade pip && pip install -r requirements_build.txt && pip install --upgrade pyinstaller && pyinstaller --noconsole --onefile --clean --name Downloader --collect-all customtkinter gui_app.py"
