# Modern YouTube Downloader

A simple, modern, and dark-themed YouTube downloader built for ease of use.

## Features

*   **Modern Interface:** Clean dark mode UI.
*   **Smart Preview:** Automatically fetches video title, thumbnail, and playlist info before downloading.
*   **Format Options:**
    *   **Best Video + Audio:** Downloads the highest quality available.
    *   **Audio Only (MP3):** Extracts audio and converts it to high-quality MP3.
*   **Playlist Support:** Detects playlists and offers to download the entire collection or just the single video.
*   **Progress Tracking:** Visual progress bars for individual files and total playlist completion.
*   **Auto-Setup:** Automatically downloads `ffmpeg` on Windows if missing (required for MP3 conversion).

## How to Use

1.  **Download:** Get the latest `Downloader.exe` from the Releases page.
2.  **Run:** Double-click the executable.
3.  **Paste Link:** Copy a YouTube video or playlist URL and paste it into the box.
4.  **Fetch Info:** Click "Fetch Info" to see the preview.
5.  **Select Options:** Choose Video or Audio, and check "Download Whole Playlist" if applicable.
6.  **Download:** Click "Download Now".
7.  **Find Files:** Your downloads will appear in a `downloads` folder next to the app.

## Development

### Requirements
*   Python 3.9+
*   `customtkinter`
*   `yt-dlp`
*   `Pillow`
*   `requests`

### Running from Source
```bash
pip install -r requirements.txt
python gui_app.py
```

### Building (Exe)
**Linux:**
```bash
pyinstaller --onefile --clean --name linux_downloader --hidden-import='PIL._tkinter_finder' gui_app.py
```

**Windows (via Docker):**
```bash
docker run --rm -v "$(pwd):/src/" --entrypoint /bin/sh cdrx/pyinstaller-windows -c "python -m pip install --upgrade pip && pip install -r requirements_build.txt && pyinstaller --noconsole --onefile --clean --name Downloader gui_app.py"
```
