"""
Module B: Audio Downloader - yt-dlp Integration

This module downloads audio from YouTube using yt-dlp.
"""

import os
import yt_dlp
import re


def sanitize_filename(filename):
    """
    Sanitize a filename by removing or replacing invalid characters.
    
    Args:
        filename (str): The filename to sanitize
    
    Returns:
        str: Sanitized filename
    """
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    return filename


def download_song(artist, title, output_dir='downloads'):
    """
    Download a song from YouTube using yt-dlp.
    
    Args:
        artist (str): Artist name
        title (str): Song title
        output_dir (str): Directory to save downloaded files (default: 'downloads')
    
    Returns:
        str: Path to the downloaded audio file, or None if download failed
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create search query
    search_query = f"{artist} {title} official audio"
    
    # Sanitize filename
    safe_artist = sanitize_filename(artist)
    safe_title = sanitize_filename(title)
    output_filename = f"{safe_artist} - {safe_title}.mp3"
    output_path = os.path.join(output_dir, output_filename)
    
    # Check if file already exists
    if os.path.exists(output_path):
        print(f"✓ File already exists: {output_filename}")
        return output_path
    
    print(f"⬇️  Downloading: {artist} - {title}")
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, f"{safe_artist} - {safe_title}.%(ext)s"),
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch1',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search and download
            ydl.download([search_query])
        
        if os.path.exists(output_path):
            print(f"✓ Downloaded: {output_filename}")
            return output_path
        else:
            print(f"❌ Download failed: File not found after download")
            return None
            
    except Exception as e:
        print(f"❌ Error downloading {artist} - {title}: {e}")
        return None


if __name__ == "__main__":
    # Test the module
    test_artist = "The Beatles"
    test_title = "Yesterday"
    
    result = download_song(test_artist, test_title)
    if result:
        print(f"\nSuccess! File saved to: {result}")
    else:
        print("\nDownload failed.")
