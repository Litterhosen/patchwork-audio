"""
Module A: Song Finder - Genius API Integration

This module searches for songs containing a specific word using the Genius API.
"""

import os
import lyricsgenius


def search_songs_with_word(word, max_results=5):
    """
    Search for songs containing a specific word using the Genius API.
    
    Args:
        word (str): The word to search for in song lyrics
        max_results (int): Maximum number of results to return (default: 5)
    
    Returns:
        list: List of dictionaries with 'artist' and 'title' keys
    
    Raises:
        ValueError: If GENIUS_API_TOKEN is not set
    """
    api_token = os.getenv('GENIUS_API_TOKEN')
    if not api_token:
        raise ValueError("GENIUS_API_TOKEN environment variable not set. Please add it to your .env file.")
    
    # Initialize Genius API client
    genius = lyricsgenius.Genius(api_token, verbose=False, remove_section_headers=True)
    
    print(f"🔍 Searching Genius for songs with the word '{word}'...")
    
    # Search for the word
    try:
        search_results = genius.search_songs(word)
    except Exception as e:
        print(f"❌ Error searching Genius API: {e}")
        return []
    
    songs = []
    for hit in search_results.get('hits', [])[:max_results]:
        result = hit.get('result', {})
        artist = result.get('primary_artist', {}).get('name', 'Unknown Artist')
        title = result.get('title', 'Unknown Title')
        
        songs.append({
            'artist': artist,
            'title': title
        })
    
    print(f"✓ Found {len(songs)} songs")
    return songs


if __name__ == "__main__":
    # Test the module
    from dotenv import load_dotenv
    load_dotenv()
    
    test_word = "love"
    results = search_songs_with_word(test_word, max_results=3)
    
    print(f"\nResults for '{test_word}':")
    for song in results:
        print(f"  - {song['artist']} - {song['title']}")
