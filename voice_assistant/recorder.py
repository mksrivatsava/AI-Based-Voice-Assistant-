"""
Microphone recorder with energy-based Voice Activity Detection (VAD).

Flow:
  1. Wait for speech to begin (RMS > SILENCE_THRESHOLD).
  2. Record until SILENCE_DURATION seconds of consecutive silence.
  3. Return audio as a float32 numpy array at SAMPLE_RATE.
"""

import numpy as np
import sounddevice as sd

import voice_assistant.config as cfg


def record_until_silence(feedback: bool = True) -> np.ndarray | None:
    chunk_size = int(cfg.SAMPLE_RATE * cfg.CHUNK_DURATION)
    silence_chunks_needed = int(cfg.SILENCE_DURATION / cfg.CHUNK_DURATION)
    max_chunks = int(cfg.MAX_RECORD_SECONDS / cfg.CHUNK_DURATION)

    audio_chunks: list[np.ndarray] = []
    silent_count = 0
    speech_started = False

    if feedback:
        print("  [Listening... speak now]")

    with sd.InputStream(
        samplerate=cfg.SAMPLE_RATE,
        channels=cfg.CHANNELS,
        dtype="float32",
    ) as stream:
        for _ in range(max_chunks):
            chunk, _ = stream.read(chunk_size)
            rms = float(np.sqrt(np.mean(chunk ** 2)))

            if rms > cfg.SILENCE_THRESHOLD:
                if not speech_started and feedback:
                    print("  [Recording...]")
                speech_started = True
                silent_count = 0
                audio_chunks.append(chunk.copy())
            elif speech_started:
                audio_chunks.append(chunk.copy())
                silent_count += 1
                if silent_count >= silence_chunks_needed:
                    break

    if not audio_chunks:
        return None

    return np.concatenate(audio_chunks, axis=0).flatten()
