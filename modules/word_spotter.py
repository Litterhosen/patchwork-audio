"""
Module C: AI Word Spotter - Whisper Integration

This module uses OpenAI Whisper to find specific words in audio files with timestamps.
"""

import whisper
import re


def find_word_timestamps(audio_file, target_word):
    """
    Use Whisper to find all occurrences of a specific word in an audio file.
    
    Args:
        audio_file (str): Path to the audio file
        target_word (str): The word to search for
    
    Returns:
        list: List of dictionaries with 'start' and 'end' times in seconds
    """
    print(f"🎧 Analyzing audio with Whisper to find '{target_word}'...")
    
    try:
        # Load the Whisper model (using base model for balance of speed and accuracy)
        model = whisper.load_model("base")
        
        # Transcribe with word-level timestamps
        result = model.transcribe(
            audio_file,
            word_timestamps=True,
            language='da'  # Danish, can be changed or auto-detected
        )
        
        # Extract word timestamps
        word_occurrences = []
        target_word_lower = target_word.lower()
        
        # Iterate through segments
        for segment in result.get('segments', []):
            for word_info in segment.get('words', []):
                word_text = word_info.get('word', '').strip().lower()
                
                # Remove punctuation for comparison
                word_text_clean = re.sub(r'[^\w\s]', '', word_text)
                
                # Check if this word matches the target word
                if word_text_clean == target_word_lower:
                    word_occurrences.append({
                        'start': word_info.get('start', 0),
                        'end': word_info.get('end', 0)
                    })
        
        print(f"✓ Found {len(word_occurrences)} occurrence(s) of '{target_word}'")
        return word_occurrences
        
    except Exception as e:
        print(f"❌ Error analyzing audio: {e}")
        return []


if __name__ == "__main__":
    # Test the module
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python word_spotter.py <audio_file> <word>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    word = sys.argv[2]
    
    timestamps = find_word_timestamps(audio_file, word)
    
    print(f"\nTimestamps for '{word}':")
    for i, ts in enumerate(timestamps, 1):
        print(f"  {i}. {ts['start']:.2f}s - {ts['end']:.2f}s")
