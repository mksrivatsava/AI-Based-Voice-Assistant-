"""
Text-to-speech using pyttsx3 (Windows SAPI5 / macOS NSSpeechSynthesizer).
Runs fully offline with no external API calls.
"""

from __future__ import annotations

import pyttsx3

import voice_assistant.config as cfg

_engine: pyttsx3.Engine | None = None


def _get_engine() -> pyttsx3.Engine:
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty("rate", cfg.TTS_RATE)
        voices = _engine.getProperty("voices")
        if voices and cfg.TTS_VOICE_INDEX < len(voices):
            _engine.setProperty("voice", voices[cfg.TTS_VOICE_INDEX].id)
    return _engine


def speak(text: str) -> None:
    """Speak text synchronously (blocks until playback is complete)."""
    engine = _get_engine()
    engine.say(text)
    engine.runAndWait()


def list_voices() -> list[str]:
    """Return names of all installed TTS voices (useful for config tuning)."""
    engine = _get_engine()
    return [v.name for v in engine.getProperty("voices")]
