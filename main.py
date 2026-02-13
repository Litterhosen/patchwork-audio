#!/usr/bin/env python3
"""
Patchwork Audio - Master Script

This is the main orchestrator that ties all modules together to create
a patchwork of audio samples from songs containing a specific word.
"""

import os
import sys
from dotenv import load_dotenv

from modules.song_finder import search_songs_with_word
from modules.audio_downloader import download_song
from modules.word_spotter import find_word_timestamps
from modules.splicer import splice_word_segments


def print_banner():
    """Print the application banner."""
    print("=" * 60)
    print("🎵  PATCHWORK AUDIO  🎵")
    print("=" * 60)
    print()


def main():
    """Main application flow."""
    print_banner()
    
    # Load environment variables
    load_dotenv()
    
    # Check if API token is set
    if not os.getenv('GENIUS_API_TOKEN'):
        print("❌ Error: GENIUS_API_TOKEN not set in .env file")
        print("Please add your Genius API token to the .env file.")
        print("See README.md for instructions.")
        sys.exit(1)
    
    # Get target word from user
    if len(sys.argv) > 1:
        target_word = sys.argv[1]
    else:
        target_word = input("Enter the word to search for: ").strip()
    
    if not target_word:
        print("❌ Error: No word provided")
        sys.exit(1)
    
    print(f"Target word: '{target_word}'")
    print()
    
    # Configure how many songs to process
    num_songs = 3
    if len(sys.argv) > 2:
        try:
            num_songs = int(sys.argv[2])
        except ValueError:
            pass
    
    # Step 1: Search for songs
    print("STEP 1: Searching for songs...")
    print("-" * 60)
    songs = search_songs_with_word(target_word, max_results=num_songs + 2)
    
    if not songs:
        print("❌ No songs found. Try a different word.")
        sys.exit(1)
    
    print()
    
    # Step 2: Download and process songs
    print("STEP 2: Downloading and processing songs...")
    print("-" * 60)
    
    total_samples = 0
    processed_songs = 0
    
    for i, song in enumerate(songs[:num_songs], 1):
        artist = song['artist']
        title = song['title']
        
        print(f"\n[{i}/{num_songs}] Processing: {artist} - {title}")
        print("-" * 40)
        
        # Download the song
        audio_file = download_song(artist, title)
        
        if not audio_file:
            print("⚠️  Skipping this song (download failed)")
            continue
        
        # Analyze with Whisper to find the word
        timestamps = find_word_timestamps(audio_file, target_word)
        
        if not timestamps:
            print(f"⚠️  Word '{target_word}' not found in this song by AI")
            continue
        
        # Splice out the segments
        output_files = splice_word_segments(audio_file, timestamps, target_word)
        
        if output_files:
            total_samples += len(output_files)
            processed_songs += 1
    
    # Step 3: Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Target word: '{target_word}'")
    print(f"Songs processed: {processed_songs}")
    print(f"Total samples created: {total_samples}")
    
    if total_samples > 0:
        print(f"\n✓ All samples saved to: output/")
        print(f"  Files are named: {target_word}_[source]_[index].wav")
        print("\n🎵 Your patchwork samples are ready!")
        print("   Import them into Ableton/FL Studio and create something unique!")
    else:
        print("\n⚠️  No samples were created.")
        print("   The word might not be found in the selected songs.")
        print("   Try a different word or check if Whisper detected the language correctly.")
    
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
