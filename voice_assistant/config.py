import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Whisper: tiny | base | small | medium | large-v3
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")   # or "cuda"
WHISPER_COMPUTE = os.getenv("WHISPER_COMPUTE", "int8") # or "float16" on GPU

# Audio recording
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 0.1          # seconds per chunk
SILENCE_THRESHOLD = 0.015     # RMS amplitude; tune to your mic
SILENCE_DURATION = 1.5        # seconds of silence before stopping
MAX_RECORD_SECONDS = 30

# TTS (pyttsx3)
TTS_RATE = 175                 # words per minute
TTS_VOICE_INDEX = 0            # 0 = first installed voice; change for female

CLAUDE_MODEL = "claude-sonnet-4-6"
CLAUDE_MAX_TOKENS = 1024

SYSTEM_PROMPT = (
    "You are a helpful, concise voice assistant. "
    "Respond naturally as if speaking out loud — keep answers brief and clear. "
    "Avoid markdown, bullet points, or any formatting that doesn't translate to speech. "
    "If you don't know something, say so plainly."
)
