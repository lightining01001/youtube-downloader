import os
import sys
import yt_dlp

def download_playlist(playlist_url, output_dir="downloads"):
    """
    Downloads videos from a YouTube playlist to a specified directory.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(playlist)s', '%(title)s.%(ext)s'), # Save as downloads/PlaylistName/Title.extension
        'format': 'bestvideo+bestaudio/best', # Best quality
        'noplaylist': False, # Ensure we download the playlist
        'ignoreerrors': True, # Continue if a video fails
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Starting download from: {playlist_url}")
            ydl.download([playlist_url])
            print("Download complete!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter the YouTube playlist URL: ")

    if url:
        download_playlist(url)
    else:
        print("No URL provided.")
    
    input("\nPress Enter to exit...")
