"""
Module D: The Splicer - Pydub Audio Processing

This module cuts out audio segments and saves them as WAV files with a "rough" aesthetic.
"""

import os
from pydub import AudioSegment


def splice_word_segments(audio_file, timestamps, word, output_dir='output'):
    """
    Cut out word segments from audio and save as individual WAV files.
    
    Args:
        audio_file (str): Path to the source audio file
        timestamps (list): List of dictionaries with 'start' and 'end' times
        word (str): The word being extracted (used for naming)
        output_dir (str): Directory to save output files (default: 'output')
    
    Returns:
        list: List of paths to the created WAV files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    if not timestamps:
        print("⚠️  No timestamps to splice")
        return []
    
    print(f"✂️  Splicing {len(timestamps)} segment(s)...")
    
    try:
        # Load the audio file
        audio = AudioSegment.from_file(audio_file)
        
        # Extract source name from filename (without extension)
        source_name = os.path.splitext(os.path.basename(audio_file))[0]
        # Sanitize source name
        source_name = source_name.replace(' ', '_')[:30]  # Limit length
        
        output_files = []
        
        for i, ts in enumerate(timestamps, 1):
            start_time = ts['start']
            end_time = ts['end']
            
            # Add 100ms buffer BEFORE the word starts (for rough aesthetic)
            buffer_ms = 100
            start_ms = max(0, int((start_time * 1000) - buffer_ms))
            end_ms = int(end_time * 1000)
            
            # Extract the segment
            segment = audio[start_ms:end_ms]
            
            # Add 50ms fade-in and fade-out to avoid clicks
            segment = segment.fade_in(50).fade_out(50)
            
            # Do NOT normalize - keep original volume for patchwork effect
            
            # Create filename
            output_filename = f"{word}_{source_name}_{i}.wav"
            output_path = os.path.join(output_dir, output_filename)
            
            # Export as WAV
            segment.export(output_path, format='wav')
            output_files.append(output_path)
            
            duration = (end_ms - start_ms) / 1000
            print(f"  ✓ {output_filename} ({duration:.2f}s)")
        
        return output_files
        
    except Exception as e:
        print(f"❌ Error splicing audio: {e}")
        return []


if __name__ == "__main__":
    # Test the module
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python splicer.py <audio_file> <word>")
        print("Example timestamps will be used for testing.")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    word = sys.argv[2]
    
    # Example timestamps for testing
    test_timestamps = [
        {'start': 10.5, 'end': 11.0},
        {'start': 25.3, 'end': 25.8}
    ]
    
    output_files = splice_word_segments(audio_file, test_timestamps, word)
    
    print(f"\nCreated {len(output_files)} file(s)")
