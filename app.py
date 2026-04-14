from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import whisper
import os
import tempfile
from werkzeug.utils import secure_filename
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'm4a', 'ogg', 'webm', 'mp4'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Model cache to avoid reloading the same model
model_cache = {}

def load_model(model_name):
    """Load a Whisper model with caching"""
    if model_name not in model_cache:
        logger.info(f"Loading Whisper model: {model_name}")
        model_cache[model_name] = whisper.load_model(model_name)
        logger.info(f"Model {model_name} loaded successfully!")
    else:
        logger.info(f"Using cached model: {model_name}")
    return model_cache[model_name]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    # Show which models are currently loaded
    loaded_models = list(model_cache.keys()) if model_cache else ['none']
    return jsonify({
        'status': 'healthy',
        'model': ', '.join(loaded_models) if model_cache else 'ready',
        'supported_formats': list(ALLOWED_EXTENSIONS)
    })

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    filepath = None
    try:
        # Check if file is present
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not supported. Allowed: {ALLOWED_EXTENSIONS}'}), 400
        
        # Get optional parameters
        model_name = request.form.get('model', 'turbo')  # Get model selection from frontend
        language = request.form.get('language', None)  # Auto-detect if None
        task = request.form.get('task', 'transcribe')  # 'transcribe' or 'translate'
        
        # Validate model name
        valid_models = ['tiny', 'base', 'small', 'medium', 'large', 'turbo']
        if model_name not in valid_models:
            return jsonify({'error': f'Invalid model. Choose from: {valid_models}'}), 400
        
        # Validate turbo + translate combination
        if model_name == 'turbo' and task == 'translate':
            return jsonify({'error': 'Turbo model does not support translation. Please use large, medium, or small model.'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"Processing file: {filename} with model: {model_name}")
        
        # Load the requested model (with caching)
        model = load_model(model_name)
        
        # Transcribe
        options = {
            'task': task,
            'fp16': False  # Use FP32 for better compatibility on Mac
        }
        
        if language:
            options['language'] = language
        
        logger.info(f"Starting transcription with options: {options}")
        result = model.transcribe(filepath, **options)
        
        # Clean up temporary file
        os.remove(filepath)
        filepath = None
        
        logger.info(f"Transcription completed for: {filename}")
        
        return jsonify({
            'success': True,
            'text': result['text'],
            'language': result.get('language', 'unknown'),
            'segments': result.get('segments', [])
        })
    
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        # Clean up file if it exists
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        return jsonify({'error': str(e)}), 500

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Return list of supported languages"""
    # Whisper supports these languages
    languages = {
        'auto': 'Auto-detect',
        'en': 'English',
        'zh': 'Chinese',
        'de': 'German',
        'es': 'Spanish',
        'ru': 'Russian',
        'ko': 'Korean',
        'fr': 'French',
        'ja': 'Japanese',
        'pt': 'Portuguese',
        'tr': 'Turkish',
        'pl': 'Polish',
        'ca': 'Catalan',
        'nl': 'Dutch',
        'ar': 'Arabic',
        'sv': 'Swedish',
        'it': 'Italian',
        'id': 'Indonesian',
        'hi': 'Hindi',
        'fi': 'Finnish',
        'vi': 'Vietnamese',
        'he': 'Hebrew',
        'uk': 'Ukrainian',
        'el': 'Greek',
        'ms': 'Malay',
        'cs': 'Czech',
        'ro': 'Romanian',
        'da': 'Danish',
        'hu': 'Hungarian',
        'ta': 'Tamil',
        'no': 'Norwegian',
        'th': 'Thai',
        'ur': 'Urdu',
        'hr': 'Croatian',
        'bg': 'Bulgarian',
        'lt': 'Lithuanian',
        'la': 'Latin',
        'mi': 'Maori',
        'ml': 'Malayalam',
        'cy': 'Welsh',
        'sk': 'Slovak',
        'te': 'Telugu',
        'fa': 'Persian',
        'lv': 'Latvian',
        'bn': 'Bengali',
        'sr': 'Serbian',
        'az': 'Azerbaijani',
        'sl': 'Slovenian',
        'kn': 'Kannada',
        'et': 'Estonian',
        'mk': 'Macedonian',
        'br': 'Breton',
        'eu': 'Basque',
        'is': 'Icelandic',
        'hy': 'Armenian',
        'ne': 'Nepali',
        'mn': 'Mongolian',
        'bs': 'Bosnian',
        'kk': 'Kazakh',
        'sq': 'Albanian',
        'sw': 'Swahili',
        'gl': 'Galician',
        'mr': 'Marathi',
        'pa': 'Punjabi',
        'si': 'Sinhala',
        'km': 'Khmer',
        'sn': 'Shona',
        'yo': 'Yoruba',
        'so': 'Somali',
        'af': 'Afrikaans',
        'oc': 'Occitan',
        'ka': 'Georgian',
        'be': 'Belarusian',
        'tg': 'Tajik',
        'sd': 'Sindhi',
        'gu': 'Gujarati',
        'am': 'Amharic',
        'yi': 'Yiddish',
        'lo': 'Lao',
        'uz': 'Uzbek',
        'fo': 'Faroese',
        'ht': 'Haitian Creole',
        'ps': 'Pashto',
        'tk': 'Turkmen',
        'nn': 'Nynorsk',
        'mt': 'Maltese',
        'sa': 'Sanskrit',
        'lb': 'Luxembourgish',
        'my': 'Myanmar',
        'bo': 'Tibetan',
        'tl': 'Tagalog',
        'mg': 'Malagasy',
        'as': 'Assamese',
        'tt': 'Tatar',
        'haw': 'Hawaiian',
        'ln': 'Lingala',
        'ha': 'Hausa',
        'ba': 'Bashkir',
        'jw': 'Javanese',
        'su': 'Sundanese'
    }
    return jsonify(languages)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎙️  Whisper Transcription Server")
    print("="*60)
    print("Models: turbo, large (loaded on demand)")
    print("Server: http://localhost:5001")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(host='127.0.0.1', port=5001, debug=False)