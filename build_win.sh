python -m pip install --upgrade pip
pip install -r requirements_build.txt
pyinstaller --onefile --clean --name download_playlist download_playlist.py
