# Whisper Local Transcription System

A secure, local audio transcription application powered by OpenAI's Whisper model. All processing happens on your machine - no data is sent to external servers.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- 🎙️ **Local Processing** - All transcription happens on your machine
- 🚀 **Multiple Models** - Choose between Turbo (fast) or Large (accurate)
- 🌐 **99 Languages** - Auto-detect or manually select from 99+ languages
- 🔄 **Translation** - Translate non-English audio to English (Large model)
- 📁 **Drag & Drop** - Easy file upload interface
- 💾 **Export Options** - Copy to clipboard or download as text file
- 📊 **Real-time Progress** - Visual feedback during transcription
- 🎨 **Modern UI** - Clean, responsive web interface

## Supported Audio Formats

MP3, WAV, FLAC, M4A, OGG, WebM, MP4 (max 500MB)

## Requirements

- **Python 3.8+
- **16GB+ RAM recommended** (8GB minimum for Turbo model)
- **FFmpeg** (for audio processing)
- **5-10GB disk space** (for Whisper models)

## Installation

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install FFmpeg

```bash
brew install ffmpeg
```

### 3. Clone the Repository

```bash
git clone https://github.com/yourusername/whisper-transcription.git
cd whisper-transcription
```

### 4. Create Virtual Environment

```bash
python3 -m venv whisper-venv
source whisper-venv/bin/activate
```

### 5. Install Dependencies

Using the included `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask flask-cors openai-whisper
```

### 6. First Run (Downloads Models)

```bash
python3 app.py
```

The first time you run the server, it will download the selected Whisper model:
- **Turbo**: ~1.5GB (first use)
- **Large**: ~3GB (first use)

Models are cached in `~/.cache/whisper/` for future use.

## Usage

### Starting the Application

#### Step 1: Start the Backend Server

```bash
# Navigate to project directory
cd whisper-transcription

# Activate virtual environment
source whisper-venv/bin/activate

# Start the Flask server
python3 app.py
```

You should see:

```
============================================================
🎙️  Whisper Transcription Server
============================================================
Models: turbo, large (loaded on demand)
Server: http://localhost:5001
Press Ctrl+C to stop
============================================================
```

#### Step 2: Open the Frontend

The frontend (`index.html`) is automatically served by the Flask backend.

**Open your web browser and navigate to:**

```
http://localhost:5001
```

The web interface will load automatically. You should see:
- A purple gradient background
- "Whisper Transcription" header
- Server status banner (green = ready)
- File upload area

### Using the Web Interface

1. **Upload Audio File**
   - Drag and drop an audio file onto the upload area, OR
   - Click the upload area to browse and select a file

2. **Configure Options**
   - **Model**: Choose between Turbo (fast) or Large (best quality)
   - **Language**: Select a specific language or leave as "Auto-detect"
   - **Task**: Choose "Transcribe" or "Translate to English"

3. **Start Transcription**
   - Click the "Start Transcription" button
   - Watch the progress bar for real-time status
   - Wait for processing to complete

4. **View and Export Results**
   - Read the transcription in the results section
   - Click "📋 Copy" to copy text to clipboard
   - Click "💾 Download" to save as a .txt file

### Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Model Comparison

| Feature | Turbo | Large |
|---------|-------|-------|
| **Speed** | 8x faster | Baseline |
| **Accuracy** | Very Good | Best |
| **VRAM Usage** | ~6 GB | ~10 GB |
| **Translation** | ❌ Not supported | ✅ Supported |
| **File Size** | 1.5 GB | 3 GB |
| **Best For** | Quick transcriptions, English content | Maximum accuracy, translation needed |

### When to Use Each Model

**Use Turbo when:**
- You need fast results
- Audio quality is good
- You're transcribing English
- You don't need translation

**Use Large when:**
- You need maximum accuracy
- Audio has background noise or accents
- You need to translate to English
- You're working with technical/specialized content

## Performance Benchmarks

On Apple M4 Pro (24GB RAM):

### Turbo Model
- **1 min audio** → ~5-10 seconds
- **10 min audio** → ~30-60 seconds
- **1 hour audio** → ~3-5 minutes

### Large Model
- **1 min audio** → ~15-20 seconds
- **10 min audio** → ~2-3 minutes
- **1 hour audio** → ~10-15 minutes

*Note: First-time model loading adds 5-10 seconds. Subsequent uses are faster due to caching.*

## Configuration

### Change Port

Edit `app.py` (last line):
```python
app.run(host='127.0.0.1', port=5001, debug=False)  # Change port here
```

And `index.html` (JavaScript section, near the top):
```javascript
const API = 'http://localhost:5001';  // Change port here
```

### Adjust File Size Limit

Edit `app.py` (line ~19):
```python
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB - change as needed
```

### Add More Models

The system supports all Whisper models:
- `tiny` (39M params, ~1GB RAM)
- `base` (74M params, ~1GB RAM)
- `small` (244M params, ~2GB RAM)
- `medium` (769M params, ~5GB RAM)
- `large` (1550M params, ~10GB RAM)
- `turbo` (809M params, ~6GB RAM)

To add more models, edit the model dropdown in `index.html`:

```html
<select id="model">
    <option value="turbo">Turbo (Fast)</option>
    <option value="large">Large (Best Quality)</option>
    <option value="medium">Medium (Balanced)</option>  <!-- Add this -->
    <option value="small">Small (Lightweight)</option>  <!-- Add this -->
</select>
```

## Project Structure

```
whisper-transcription/
├── app.py              # Flask backend server
├── index.html          # Web interface (frontend)
├── requirements.txt    # Python dependencies
├── whisper-venv/       # Virtual environment (not in git)
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT License
└── README.md          # This file
```

## Troubleshooting

### Port 5000 Already in Use

macOS uses port 5000 for AirPlay Receiver. This app uses port 5001 by default.

To use port 5000 instead:
1. **System Settings** → **General** → **AirDrop & Handoff**
2. Turn off **AirPlay Receiver**
3. Update port in both `app.py` and `index.html`

### Server Won't Start

```bash
# Check if virtual environment is activated
source whisper-venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check Python version (should be 3.8-3.12)
python3 --version
```

### Frontend Shows "Server not running"

1. Make sure the backend is running (`python3 app.py`)
2. Check the terminal for error messages
3. Verify you're accessing `http://localhost:5001` (not 5000)
4. Check browser console for errors (F12 → Console tab)

### Slow Transcription

- Use **Turbo** model for faster processing
- Close other applications to free up RAM
- Ensure your Mac is plugged in (performance throttles on battery)
- Try shorter audio segments (split long files)

### "Module not found" Error

```bash
# Make sure you're in the virtual environment
source whisper-venv/bin/activate

# Reinstall all dependencies
pip install -r requirements.txt
```

### FFmpeg Not Found

```bash
# Reinstall FFmpeg
brew reinstall ffmpeg

# Verify installation
ffmpeg -version
```

### "Turbo cannot translate" Error

The Turbo model does not support translation. To translate audio:
1. Select the **Large** model (or medium/small)
2. Choose **"Translate to English"** task
3. Upload your non-English audio file

### Model Download Fails

If model download is interrupted:

```bash
# Clear the cache
rm -rf ~/.cache/whisper/

# Restart the server (it will re-download)
python3 app.py
```

### Browser Can't Connect

```bash
# Check if server is running
# You should see the server banner in terminal

# Try accessing with explicit IP
http://127.0.0.1:5001

# Check firewall settings
# System Settings → Network → Firewall
```

## Security & Privacy

- ✅ **All processing is local** - no data sent to external servers
- ✅ **Temporary files** are automatically deleted after transcription
- ✅ **No internet required** after initial model download
- ✅ **No logging** of transcription content
- ✅ **Open source** - inspect the code yourself
- ✅ **No cookies or tracking**

## Supported Languages

Afrikaans, Arabic, Armenian, Assamese, Azerbaijani, Bashkir, Basque, Belarusian, Bengali, Bosnian, Breton, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Faroese, Finnish, French, Galician, Georgian, German, Greek, Gujarati, Haitian Creole, Hausa, Hawaiian, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Javanese, Kannada, Kazakh, Khmer, Korean, Lao, Latin, Latvian, Lingala, Lithuanian, Luxembourgish, Macedonian, Malagasy, Malay, Malayalam, Maltese, Marathi, Mongolian, Myanmar, Nepali, Norwegian, Nynorsk, Occitan, Pashto, Persian, Polish, Portuguese, Punjabi, Romanian, Russian, Sanskrit, Serbian, Shona, Sindhi, Sinhala, Slovak, Slovenian, Somali, Spanish, Sundanese, Swahili, Swedish, Tagalog, Tajik, Tamil, Tatar, Telugu, Thai, Tibetan, Turkish, Turkmen, Ukrainian, Urdu, Uzbek, Vietnamese, Welsh, Yiddish, Yoruba

## Advanced Usage

### Command Line Transcription

You can also use Whisper directly from the command line:

```bash
# Activate virtual environment
source whisper-venv/bin/activate

# Transcribe a file
whisper audio.mp3 --model turbo --language English

# Translate to English
whisper audio.mp3 --model large --task translate

# Output to specific format
whisper audio.mp3 --model turbo --output_format txt
```

### Batch Processing

For multiple files, create a simple script:

```bash
#!/bin/bash
for file in *.mp3; do
    whisper "$file" --model turbo --output_dir ./transcriptions/
done
```

### API Usage

You can also call the API directly:

```bash
curl -X POST http://localhost:5001/api/transcribe \
  -F "audio=@audio.mp3" \
  -F "model=turbo" \
  -F "task=transcribe"
```

## Development

### Running in Debug Mode

Edit `app.py` (last line):
```python
app.run(host='127.0.0.1', port=5001, debug=True)  # Enable debug mode
```

Debug mode provides:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

### Modifying the Frontend

The frontend is a single HTML file (`index.html`) with inline CSS and JavaScript. No build process required - just edit and refresh!

## Known Issues

- Python 3.13 may have compatibility issues with some dependencies
- Very large files (>500MB) may cause memory issues
- Translation quality varies by language pair
- Turbo model does not support translation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - The amazing speech recognition model
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [FFmpeg](https://ffmpeg.org/) - Audio processing

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review the [Whisper GitHub Issues](https://github.com/openai/whisper/issues)
3. Open an issue in this repository with:
   - Your Python version (`python3 --version`)
   - Your OS version
   - Error messages from the terminal
   - Steps to reproduce the issue

## FAQ

**Q: Can I use this offline?**  
A: Yes! After the initial model download, no internet connection is required.

**Q: How accurate is the transcription?**  
A: The Large model achieves near-human accuracy for clear audio. Accuracy depends on audio quality, accents, and background noise.

**Q: Can I transcribe video files?**  
A: Yes! The system automatically extracts audio from video files (MP4, WebM, etc.).

**Q: Is there a file size limit?**  
A: Default is 500MB. You can change this in `app.py`.

**Q: Can I run this on Windows or Linux?**  
A: The code is cross-platform, but installation steps differ. This guide is optimized for macOS.

**Q: How do I update Whisper?**  
A: Run `pip install --upgrade openai-whisper` in your virtual environment.

**Q: Can I use this commercially?**  
A: Yes! Both this project and Whisper are MIT licensed.

## Changelog

### Version 1.0 (Current)
- ✨ Added dynamic model selection (Turbo/Large)
- 🔧 Changed default port to 5001 (avoid macOS AirPlay conflict)
- ⚡ Added model caching for faster switching
- 🛡️ Improved error handling and validation
- 🎨 Updated UI with model selection dropdown
- 📝 Added comprehensive documentation

---