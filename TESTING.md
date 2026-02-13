# 🧪 Test Guide - Patchwork Audio

Denne guide hjælper dig med at teste og afprøve Patchwork Audio applikationen.

## 🚀 Hurtig Start - Test Setup

### 1. Verificer forudsætninger

Først skal du sikre dig at alle forudsætninger er opfyldt:

```bash
# Tjek Python version (skal være 3.8+)
python3 --version

# Tjek at FFmpeg er installeret
ffmpeg -version
```

Hvis FFmpeg mangler, installer det:
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download fra https://ffmpeg.org/download.html

### 2. Kør setup script

```bash
# Linux/macOS
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

### 3. Aktiver virtual environment

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate.bat
```

### 4. Få en Genius API Token

Dette er **nødvendigt** for at søge efter sange:

1. Gå til https://genius.com/api-clients
2. Log ind (eller opret en gratis konto)
3. Klik "New API Client"
4. Udfyld formularen:
   - **App Name**: `Patchwork Audio Test` (eller hvad som helst)
   - **App Website URL**: `http://localhost` (eller hvad som helst)
5. Klik "Save"
6. Kopier din "Client Access Token"
7. Tilføj den til `.env` filen:

```bash
echo "GENIUS_API_TOKEN=din_faktiske_token_her" > .env
```

## 🧪 Test de individuelle moduler

Du kan teste hvert modul individuelt for at sikre at alt virker:

### Test Modul A: Song Finder (Genius API)

```bash
python3 -c "
from dotenv import load_dotenv
load_dotenv()
from modules.song_finder import search_songs_with_word

songs = search_songs_with_word('love', max_results=3)
print(f'\n✓ Fandt {len(songs)} sange:')
for song in songs:
    print(f\"  - {song['artist']} - {song['title']}\")
"
```

**Forventet output**: En liste med 3 sange der indeholder ordet "love"

### Test Modul B: Audio Downloader (yt-dlp)

```bash
python3 -c "
from modules.audio_downloader import download_song

print('Testing download...')
file = download_song('Rick Astley', 'Never Gonna Give You Up')
if file:
    print(f'✓ Success! Downloaded til: {file}')
else:
    print('✗ Download fejlede')
"
```

**Forventet output**: En MP3 fil i `downloads/` mappen

**Note**: Første download kan tage lidt tid. Efterfølgende downloads af samme sang vil være hurtige (cached).

### Test Modul C: Word Spotter (Whisper AI)

Først skal du have en audio fil. Brug filen fra forrige test:

```bash
python3 << 'EOF'
from modules.word_spotter import find_word_timestamps
import os

# Find første MP3 fil i downloads/
audio_files = [f for f in os.listdir('downloads') if f.endswith('.mp3')]
if audio_files:
    audio_path = os.path.join('downloads', audio_files[0])
    print(f"Analyserer: {audio_files[0]}")
    
    timestamps = find_word_timestamps(audio_path, 'never')
    print(f"\n✓ Fandt '{timestamps}' forekomster af ordet 'never'")
    for i, ts in enumerate(timestamps, 1):
        print(f"  {i}. {ts['start']:.2f}s - {ts['end']:.2f}s")
else:
    print("⚠️  Ingen MP3 filer fundet. Kør først download test.")
EOF
```

**Forventet output**: Tidsstempler for hver forekomst af ordet

**Note**: Første gang Whisper køres, downloader den en AI-model (~150MB). Dette kan tage lidt tid.

### Test Modul D: Splicer (Pydub)

```bash
python3 << 'EOF'
from modules.splicer import splice_word_segments
import os

# Find første MP3 fil
audio_files = [f for f in os.listdir('downloads') if f.endswith('.mp3')]
if audio_files:
    audio_path = os.path.join('downloads', audio_files[0])
    
    # Test med dummy timestamps
    test_timestamps = [
        {'start': 10.0, 'end': 10.5},
        {'start': 20.0, 'end': 20.5}
    ]
    
    output_files = splice_word_segments(audio_path, test_timestamps, 'test')
    print(f"\n✓ Skabte {len(output_files)} WAV filer:")
    for f in output_files:
        print(f"  - {f}")
else:
    print("⚠️  Ingen MP3 filer fundet. Kør først download test.")
EOF
```

**Forventet output**: WAV filer i `output/` mappen

## 🎵 Test den fulde applikation

Nu kan du teste hele flowet:

### Simpel test med et almindeligt ord

```bash
python main.py love
```

Dette vil:
1. Søge efter sange med ordet "love"
2. Downloade 3 sange
3. Analysere dem med Whisper
4. Udskære alle forekomster af "love"
5. Gemme WAV filer i `output/`

### Test med et dansk ord

```bash
python main.py kaffe
```

### Test med flere sange

```bash
python main.py love 5
```

## 🔍 Verificer output

Efter en succesfuld kørsel:

```bash
# Se downloadede sange
ls -lh downloads/

# Se genererede samples
ls -lh output/

# Afspil et sample (Linux/macOS)
afplay output/love_*.wav  # macOS
aplay output/love_*.wav   # Linux
```

På Windows kan du åbne `output/` mappen i File Explorer og dobbeltklikke på WAV filerne.

## ❓ Troubleshooting

### Problem: "GENIUS_API_TOKEN not set"

**Løsning**: Du har ikke tilføjet din Genius API token til `.env` filen.

```bash
# Tjek om .env filen eksisterer
cat .env

# Hvis den mangler, opret den:
cp .env.example .env
# Rediger derefter filen og tilføj din token
```

### Problem: "FFmpeg not found"

**Løsning**: FFmpeg er ikke installeret eller ikke i PATH.

```bash
# Test om FFmpeg er tilgængelig
which ffmpeg  # Linux/macOS
where ffmpeg  # Windows

# Installer FFmpeg hvis den mangler (se instruktioner øverst)
```

### Problem: "ModuleNotFoundError"

**Løsning**: Dependencies er ikke installeret.

```bash
# Aktiver virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat  # Windows

# Installer dependencies
pip install -r requirements.txt
```

### Problem: Download fejler

**Løsninger**:
1. Tjek din internetforbindelse
2. Nogle videoer er ikke tilgængelige i dit land
3. YouTube kan nogle gange blokere for mange requests - vent lidt og prøv igen
4. Tjek at yt-dlp er up-to-date: `pip install --upgrade yt-dlp`

### Problem: Whisper finder ikke ordet

**Mulige årsager**:
1. Ordet udtales anderledes end det staves
2. Baggrundsstøj gør det svært for AI'en at høre
3. Ordet er meget hurtigt udtalt
4. Forkert sprog (Whisper er sat til dansk, men kan også håndtere engelsk)

**Tips**: Prøv med almindelige ord først (love, time, day) før du tester med sjældne ord.

### Problem: "Out of memory" eller langsom performance

**Løsning**: 
- Whisper 'base' modellen bruges som standard (balanceret)
- Hvis du har en kraftig computer, kan du bruge 'small' eller 'medium' for bedre nøjagtighed
- Hvis du har en langsom computer, kan du bruge 'tiny' for hurtigere processing
- Rediger `modules/word_spotter.py` linje 26: `model = whisper.load_model("base")`
- Skift "base" til "tiny", "small", "medium" eller "large"

## 📊 Forventet performance

- **Song search**: < 5 sekunder
- **Download**: 30-60 sekunder per sang
- **Whisper analyse**: 1-3 minutter per sang (afhænger af længde og computer)
- **Splicing**: < 5 sekunder

En komplet kørsel med 3 sange tager typisk 5-10 minutter første gang (pga. Whisper model download).
Efterfølgende kørsler er hurtigere.

## 🎨 Test "Patchwork" æstetikken

For at høre den karakteristiske "patchwork" lyd:

1. Kør applikationen med samme ord på forskellige genres:
   ```bash
   # Brug et generisk ord som "love" eller "time"
   python main.py love 5
   ```

2. Importer alle WAV filer fra `output/` ind i Ableton/FL Studio

3. Læg dem på forskellige tracks og afspil dem efter hinanden

4. Bemærk:
   - **Forskellig lydstyrke**: Gamle sange er stille, moderne er høje
   - **Forskellig karakter**: Hver sample har sin egen "vibe"
   - **Pre-buffer**: Du hører lidt af den originale sang før ordet
   - **Ingen polering**: Råt og autentisk

Det er DET der er patchwork-æstetikken! 🎵

## 🎯 Næste skridt

Når alt virker:

1. Eksperimenter med forskellige ord
2. Prøv både engelske og danske ord
3. Import samples i din DAW
4. Lav noget vildt! 🚀

---

Har du stadig problemer? Opret et issue på GitHub: https://github.com/Litterhosen/patchwork-audio/issues
