from gtts import gTTS
import tempfile

def text_to_audio_bytes(text: str, lang: str = "en"):
    tts = gTTS(text=text, lang=lang)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        filename = fp.name

        
    tts.save(filename)

    with open(filename, "rb") as f:
        return f.read()