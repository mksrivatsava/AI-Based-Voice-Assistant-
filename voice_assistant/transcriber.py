"""
Speech-to-text using faster-whisper (CTranslate2 backend).

The model is loaded once on first use and reused for subsequent calls
to avoid the cold-start penalty on every utterance.
"""

from __future__ import annotations

import numpy as np
from faster_whisper import WhisperModel

import voice_assistant.config as cfg

_model: WhisperModel | None = None


def _get_model() -> WhisperModel:
    global _model
    if _model is None:
        print(f"  [Loading Whisper '{cfg.WHISPER_MODEL}' — one-time download if needed]")
        _model = WhisperModel(
            cfg.WHISPER_MODEL,
            device=cfg.WHISPER_DEVICE,
            compute_type=cfg.WHISPER_COMPUTE,
        )
    return _model


def transcribe(audio: np.ndarray) -> str:
    """Transcribe a float32 audio array; returns stripped text or empty string."""
    model = _get_model()
    segments, _ = model.transcribe(
        audio,
        beam_size=5,
        language="en",
        vad_filter=True,           # built-in VAD removes silence before decoding
        vad_parameters={"min_silence_duration_ms": 500},
    )
    return " ".join(seg.text.strip() for seg in segments).strip()
