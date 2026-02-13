# 🎵 Patchwork Audio

En Python-applikation der søger efter sange med et specifikt ord, downloader dem, finder ordets præcise tidsstempler ved hjælp af AI, og skærer ordet ud som .wav-filer klar til brug i Ableton/FL Studio.

Applikationen producerer bevidst "rough" og "patchwork"-lydende output — ikke poleret eller normaliseret. Det er meningen at samples skal have forskellig lydstyrke og karakter for at skabe en unik, collage-agtig lydoplevelse.

## ✨ Features

- 🔍 **Søger efter sange** med et specifikt ord via Genius API
- ⬇️ **Downloader audio** fra YouTube i høj kvalitet
- 🎧 **AI-baseret ord-detektion** med OpenAI Whisper (word-level timestamps)
- ✂️ **Automatisk udskæring** af ord-segmenter som individuelle WAV-filer
- 🎨 **"Rough" æstetik** med 100ms pre-buffer og ingen volume-normalisering
- 🎵 **DAW-klar** til import i Ableton, FL Studio, eller andre DAWs

## 📋 Krav

- Python 3.8 eller nyere
- FFmpeg (til audio-behandling)
- Genius API token (gratis fra https://genius.com/api-clients)

## 🚀 Installation

### 1. Klon repository

```bash
git clone https://github.com/Litterhosen/patchwork-audio.git
cd patchwork-audio
```

### 2. Installer FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download fra https://ffmpeg.org/download.html og tilføj til PATH

### 3. Kør setup-script

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

Dette vil:
- Oprette et virtual environment
- Installere alle Python-dependencies
- Oprette nødvendige mapper
- Opsætte .env fil

### 4. Tilføj din Genius API Token

1. Gå til https://genius.com/api-clients
2. Log ind eller opret en konto
3. Klik "New API Client"
4. Udfyld formular (app name, url kan være hvad som helst)
5. Kopier din "Client Access Token"
6. Åbn `.env` filen og tilføj din token:

```
GENIUS_API_TOKEN=din_token_her
```

## 💻 Brug

### Basis anvendelse

```bash
# Aktiver virtual environment (hvis ikke allerede aktivt)
source venv/bin/activate  # Linux/macOS
# ELLER
venv\Scripts\activate.bat  # Windows

# Kør applikationen
python main.py
```

Du vil blive bedt om at indtaste et ord at søge efter. Applikationen vil derefter:
1. Søge efter sange med dette ord
2. Downloade 3-5 sange
3. Analysere hver sang med AI
4. Udskære alle forekomster af ordet
5. Gemme som `.wav` filer i `output/` mappen

### Kommandolinje argumenter

```bash
# Specificer ord direkte
python main.py kaffe

# Specificer ord og antal sange
python main.py kaffe 5
```

### Eksempel output

```
🎵  PATCHWORK AUDIO  🎵
Target word: 'kaffe'

STEP 1: Searching for songs...
🔍 Searching Genius for songs with the word 'kaffe'...
✓ Found 5 songs

STEP 2: Downloading and processing songs...
[1/3] Processing: Artist Name - Song Title
⬇️  Downloading: Artist Name - Song Title
✓ Downloaded: Artist_Name_-_Song_Title.mp3
🎧 Analyzing audio with Whisper to find 'kaffe'...
✓ Found 2 occurrence(s) of 'kaffe'
✂️  Splicing 2 segment(s)...
  ✓ kaffe_Artist_Name_Song_Title_1.wav (0.65s)
  ✓ kaffe_Artist_Name_Song_Title_2.wav (0.58s)

SUMMARY
Target word: 'kaffe'
Songs processed: 3
Total samples created: 6

✓ All samples saved to: output/
  Files are named: kaffe_[source]_[index].wav

🎵 Your patchwork samples are ready!
   Import them into Ableton/FL Studio and create something unique!
```

## 📁 Projekt struktur

```
patchwork-audio/
├── main.py                    # Hoved-script der orkestrerer alt
├── requirements.txt           # Python dependencies
├── setup.sh                   # Setup script til Linux/macOS
├── setup.bat                  # Setup script til Windows
├── README.md                  # Denne fil
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore regler
├── modules/                   # App moduler
│   ├── __init__.py
│   ├── song_finder.py        # Modul A: Genius API søgning
│   ├── audio_downloader.py   # Modul B: YouTube download
│   ├── word_spotter.py       # Modul C: Whisper AI analyse
│   └── splicer.py            # Modul D: Audio udskæring
├── downloads/                 # Downloaded MP3 filer (gitignored)
└── output/                    # Genererede WAV samples (gitignored)
```

## 🎨 Den "Patchwork" Æstetik

Denne app er designet til at producere intentionelt **rough** og **upoleret** output:

1. **100ms Pre-Buffer**: Hver sample inkluderer 100ms før ordet starter, så du får noget af støjen/lead-in fra originalen
2. **Ingen Normalisering**: Lydstyrken er forskellig mellem samples. En gammel jazz-sang vil være stille, mens en moderne pop-sang vil være højere - det er meningen!
3. **50ms Fade**: Korte fades for at undgå clicks, men ikke nok til at polere lyden
4. **Forskellige kilder**: Ved at kombinere samples fra forskellige årtier og genrer får du en unik collage-lyd

Dette gør samples perfekte til:
- Lo-fi hip hop beats
- Eksperimentel elektronisk musik
- Sampling-baseret komposition
- Audio-collages
- Kreativ lyddesign

## 🔧 Moduler

### Modul A: Song Finder (`modules/song_finder.py`)
Bruger Genius API til at søge efter sange med et specifikt ord i teksten.

### Modul B: Audio Downloader (`modules/audio_downloader.py`)
Downloader audio fra YouTube ved hjælp af yt-dlp i høj kvalitet (192kbps MP3).

### Modul C: AI Word Spotter (`modules/word_spotter.py`)
Bruger OpenAI Whisper til at transskribere audio med word-level timestamps og finde præcise placeringer af target-ordet.

### Modul D: The Splicer (`modules/splicer.py`)
Skærer audio-segmenter ud med Pydub og gemmer som individuelle WAV-filer med fade-in/out.

## ⚠️ Bemærkninger

- **Første kørsel**: Whisper vil downloade sin AI-model (ca. 150MB for 'base' modellen)
- **Sprog**: Whisper er sat til dansk ('da'), men virker også på engelsk
- **Processing tid**: AI-analysen tager tid - vær tålmodig!
- **Download fejl**: Nogle sange kan ikke findes på YouTube - applikationen skipper automatisk disse
- **API limits**: Genius API har rate limits - undgå at køre mange søgninger hurtigt efter hinanden

## 🤝 Bidrag

Pull requests er velkomne! For større ændringer, åbn venligst et issue først for at diskutere hvad du gerne vil ændre.

## 📄 Licens

MIT

## 🙏 Credits

Lavet med ❤️ af danske musikproducenter til danske musikproducenter.

Bygget med:
- [lyricsgenius](https://github.com/johnwmillr/LyricsGenius) - Genius API wrapper
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition AI
- [Pydub](https://github.com/jiaaro/pydub) - Audio manipulation

---

**Lav noget vildt! 🎵**
