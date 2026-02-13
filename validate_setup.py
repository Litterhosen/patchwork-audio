#!/usr/bin/env python3
"""
Patchwork Audio - Setup Validator
Checks if your system is ready to run Patchwork Audio.
"""

import sys
import os
import subprocess

def print_header():
    print("=" * 70)
    print("🔍 PATCHWORK AUDIO - SETUP VALIDATOR")
    print("=" * 70)
    print()

def check_python_version():
    """Check if Python version is 3.8+"""
    print("1. Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} (skal være 3.8+)")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print("2. Checking FFmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"   ✓ {version_line}")
            return True
        else:
            print("   ✗ FFmpeg ikke fundet")
            return False
    except FileNotFoundError:
        print("   ✗ FFmpeg ikke installeret")
        print("      Installer med:")
        print("      - Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("      - macOS: brew install ffmpeg")
        print("      - Windows: https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        print(f"   ⚠ Kunne ikke tjekke FFmpeg: {e}")
        return False

def check_virtual_env():
    """Check if virtual environment exists"""
    print("3. Checking virtual environment...")
    if os.path.exists('venv') or os.path.exists('env'):
        print("   ✓ Virtual environment fundet")
        return True
    else:
        print("   ⚠ Virtual environment ikke fundet")
        print("      Kør setup.sh eller setup.bat først")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("4. Checking Python dependencies...")
    
    required_packages = [
        'lyricsgenius',
        'yt_dlp',
        'whisper',
        'pydub',
        'dotenv'
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} ikke installeret")
            all_ok = False
    
    if not all_ok:
        print("      Installer med: pip install -r requirements.txt")
    
    return all_ok

def check_env_file():
    """Check if .env file exists and has API token"""
    print("5. Checking .env configuration...")
    
    if not os.path.exists('.env'):
        print("   ⚠ .env fil mangler")
        print("      Kopier .env.example til .env og tilføj din Genius API token")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
    
    if 'GENIUS_API_TOKEN' in content:
        # Check if token is not placeholder
        if 'your_token_here' in content or content.strip() == 'GENIUS_API_TOKEN=':
            print("   ⚠ .env fil eksisterer, men API token er ikke sat")
            print("      Tilføj din Genius API token til .env filen")
            print("      Få en token på: https://genius.com/api-clients")
            return False
        else:
            print("   ✓ .env fil konfigureret")
            return True
    else:
        print("   ⚠ .env fil mangler GENIUS_API_TOKEN")
        return False

def check_directories():
    """Check if required directories exist"""
    print("6. Checking project directories...")
    
    dirs = ['modules', 'downloads', 'output']
    all_ok = True
    
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"   ✓ {dir_name}/")
        else:
            print(f"   ⚠ {dir_name}/ mangler (vil blive oprettet automatisk)")
            all_ok = False
    
    return True  # Not critical, can be created

def check_modules():
    """Check if all module files exist"""
    print("7. Checking application modules...")
    
    modules = [
        'modules/__init__.py',
        'modules/song_finder.py',
        'modules/audio_downloader.py',
        'modules/word_spotter.py',
        'modules/splicer.py'
    ]
    
    all_ok = True
    for module in modules:
        if os.path.exists(module):
            print(f"   ✓ {module}")
        else:
            print(f"   ✗ {module} mangler")
            all_ok = False
    
    return all_ok

def main():
    print_header()
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    
    checks = [
        ("Python", check_python_version),
        ("FFmpeg", check_ffmpeg),
        ("Virtual Environment", check_virtual_env),
        ("Dependencies", check_dependencies),
        ("Environment Variables", check_env_file),
        ("Directories", check_directories),
        ("Modules", check_modules)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ✗ Error checking {name}: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"  {status} {name}")
    
    print()
    print(f"Checks passed: {passed}/{total}")
    print()
    
    if passed == total:
        print("✅ Din setup er klar! Du kan nu køre:")
        print("   python main.py")
        print()
        print("Se TESTING.md for test-instruktioner og eksempler.")
        return 0
    else:
        print("⚠️  Nogle checks fejlede. Fix problemerne ovenfor og kør dette script igen.")
        print()
        print("Hurtig hjælp:")
        print("  1. Kør setup.sh eller setup.bat først")
        print("  2. Aktiver virtual environment: source venv/bin/activate")
        print("  3. Tilføj Genius API token til .env filen")
        print()
        print("Se TESTING.md for detaljerede instruktioner.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
