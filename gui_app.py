import re
import customtkinter as ctk
import yt_dlp
import threading
import os
import requests
from PIL import Image
from io import BytesIO

# Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern YouTube Downloader")
        self.geometry("600x750")
        self.resizable(False, False)

        # Data placeholders
        self.download_info = None
        self.is_playlist = False
        self.output_dir = "downloads"
        
        # --- UI Layout ---
        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header = ctk.CTkLabel(self, text="YouTube Downloader", font=("Roboto", 24, "bold"))
        self.header.pack(pady=20)

        # URL Input
        self.url_frame = ctk.CTkFrame(self)
        self.url_frame.pack(pady=10, padx=20, fill="x")
        
        self.url_entry = ctk.CTkEntry(self.url_frame, placeholder_text="Paste YouTube Link Here...", height=40)
        self.url_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        self.fetch_btn = ctk.CTkButton(self.url_frame, text="Fetch Info", width=100, height=40, command=self.start_fetch_info)
        self.fetch_btn.pack(side="right")

        # Preview Section
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.pack(pady=20, padx=20, fill="x")
        
        self.thumb_label = ctk.CTkLabel(self.preview_frame, text="No Video Loaded", height=150, corner_radius=10, fg_color="#333")
        self.thumb_label.pack(pady=10, padx=10, fill="x")
        
        self.title_label = ctk.CTkLabel(self.preview_frame, text="", font=("Roboto", 16), wraplength=500)
        self.title_label.pack(pady=5)
        
        self.info_label = ctk.CTkLabel(self.preview_frame, text="", text_color="gray")
        self.info_label.pack(pady=(0, 10))

        # Options
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(pady=10, padx=20, fill="x")
        
        self.format_var = ctk.StringVar(value="video")
        self.radio_video = ctk.CTkRadioButton(self.options_frame, text="Best Video + Audio", variable=self.format_var, value="video")
        self.radio_video.pack(side="left", padx=20, pady=10)
        
        self.radio_audio = ctk.CTkRadioButton(self.options_frame, text="Audio Only (MP3)", variable=self.format_var, value="audio")
        self.radio_audio.pack(side="left", padx=20, pady=10)

        self.playlist_var = ctk.BooleanVar(value=True)
        self.playlist_check = ctk.CTkCheckBox(self.options_frame, text="Download Whole Playlist", variable=self.playlist_var)
        # Initially hidden, shown if playlist detected
        
        # Progress Section
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.pack(pady=20, padx=20, fill="x")

        self.status_label = ctk.CTkLabel(self.progress_frame, text="Ready", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=(10, 0))

        self.pbar_file_label = ctk.CTkLabel(self.progress_frame, text="Current File:", anchor="w", font=("Roboto", 12))
        self.pbar_file_label.pack(fill="x", padx=10, pady=(5, 0))
        self.pbar_file = ctk.CTkProgressBar(self.progress_frame)
        self.pbar_file.pack(fill="x", padx=10, pady=5)
        self.pbar_file.set(0)

        self.pbar_total_label = ctk.CTkLabel(self.progress_frame, text="Total Progress:", anchor="w", font=("Roboto", 12))
        self.pbar_total_label.pack(fill="x", padx=10, pady=(5, 0))
        self.pbar_total = ctk.CTkProgressBar(self.progress_frame)
        self.pbar_total.pack(fill="x", padx=10, pady=5)
        self.pbar_total.set(0)

        # Download Button
        self.download_btn = ctk.CTkButton(self, text="Download Now", height=50, font=("Roboto", 18, "bold"), command=self.start_download, state="disabled")
        self.download_btn.pack(pady=20, padx=20, fill="x")

    # --- Logic ---

    def start_fetch_info(self):
        url = self.url_entry.get()
        if not url:
            return
        
        self.fetch_btn.configure(state="disabled")
        self.status_label.configure(text="Fetching metadata...")
        threading.Thread(target=self.fetch_info, args=(url,), daemon=True).start()

    def fetch_info(self, url):
        ydl_opts = {'quiet': True, 'extract_flat': 'in_playlist'}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.download_info = info
                self.is_playlist = 'entries' in info

                # Update UI
                self.after(0, self.update_preview, info)
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)}"))
        finally:
            self.after(0, lambda: self.fetch_btn.configure(state="normal"))

    def update_preview(self, info):
        title = info.get('title', 'Unknown Title')
        thumb_url = info.get('thumbnails', [{}])[-1].get('url')
        
        self.title_label.configure(text=title)
        
        if self.is_playlist:
            count = len(list(info.get('entries', [])))
            self.info_label.configure(text=f"Playlist • {count} Videos")
            self.playlist_check.pack(side="left", padx=20, pady=10)
            self.playlist_check.select()
        else:
            self.info_label.configure(text="Single Video")
            self.playlist_check.pack_forget()

        self.download_btn.configure(state="normal")
        self.status_label.configure(text="Ready to download.")

        # Fetch Thumbnail Image
        if thumb_url:
            threading.Thread(target=self.load_thumbnail, args=(thumb_url,), daemon=True).start()

    def load_thumbnail(self, url):
        try:
            response = requests.get(url)
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            
            # Resize keeping aspect ratio
            base_width = 300
            w_percent = (base_width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(base_width, h_size))
            self.after(0, lambda: self.thumb_label.configure(image=ctk_img, text=""))
        except:
            pass

    def check_ffmpeg(self):
        """Checks if ffmpeg exists, downloads it if not (Windows only logic mostly, but safe elsewhere)."""
        ffmpeg_exe = "ffmpeg.exe" if os.name == 'nt' else "ffmpeg"
        if os.path.exists(ffmpeg_exe):
            return ffmpeg_exe
        
        # If on Windows and missing, try to download
        if os.name == 'nt':
            self.after(0, lambda: self.status_label.configure(text="Downloading required component (FFmpeg)..."))
            try:
                # URL for a lightweight static build of ffmpeg
                url = "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/ffmpeg-win32-ia32.exe"
                response = requests.get(url, stream=True)
                with open(ffmpeg_exe, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return ffmpeg_exe
            except Exception as e:
                print(f"Failed to download ffmpeg: {e}")
                return None
        return None

    def start_download(self):
        url = self.url_entry.get()
        if not url: return

        self.download_btn.configure(state="disabled")
        self.url_entry.configure(state="disabled")
        self.radio_audio.configure(state="disabled")
        self.radio_video.configure(state="disabled")
        
        threading.Thread(target=self.download_process, args=(url,), daemon=True).start()

    def download_process(self, url):
        # Ensure FFmpeg is available
        ffmpeg_path = self.check_ffmpeg()

        fmt = self.format_var.get()
        is_playlist_dl = self.playlist_var.get() if self.is_playlist else False
        
        # Reset bars
        self.after(0, lambda: self.pbar_file.set(0))
        self.after(0, lambda: self.pbar_total.set(0))

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        ydl_opts = {
            'outtmpl': os.path.join(self.output_dir, '%(playlist_title)s', '%(title)s.%(ext)s') if is_playlist_dl else os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'noplaylist': not is_playlist_dl,
            'progress_hooks': [self.progress_hook],
            'ignoreerrors': True,
        }

        if ffmpeg_path:
             ydl_opts['ffmpeg_location'] = os.path.abspath(ffmpeg_path)

        if fmt == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
            })
        else:
            ydl_opts.update({'format': 'bestvideo+bestaudio/best'})

        # If playlist, we try to estimate total items for the total progress bar
        self.total_items = len(list(self.download_info.get('entries', []))) if self.is_playlist and is_playlist_dl else 1
        self.current_item = 0

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.after(0, lambda: self.status_label.configure(text="All downloads complete!", text_color="green"))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {e}", text_color="red"))
        finally:
            self.after(0, self.reset_ui)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # File Progress
            try:
                # Remove ANSI escape codes and the % symbol
                percent_str = d.get('_percent_str', '0%')
                clean_percent = re.sub(r'\x1b\[[0-9;]*m', '', percent_str).replace('%', '').strip()
                self.after(0, lambda: self.pbar_file.set(float(clean_percent)/100))
            except Exception as e: 
                pass
            
            # Status Text
            filename = d.get('info_dict', {}).get('title', 'Unknown')
            # Truncate filename
            if len(filename) > 40: filename = filename[:37] + "..."
            
            msg = f"Downloading: {filename}"
            self.after(0, lambda: self.status_label.configure(text=msg))

        elif d['status'] == 'finished':
            self.current_item += 1
            total_prog = self.current_item / self.total_items if self.total_items > 0 else 1
            self.after(0, lambda: self.pbar_total.set(total_prog))
            self.after(0, lambda: self.pbar_file.set(1)) # Fill current bar

    def reset_ui(self):
        self.download_btn.configure(state="normal")
        self.url_entry.configure(state="normal")
        self.radio_audio.configure(state="normal")
        self.radio_video.configure(state="normal")

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
