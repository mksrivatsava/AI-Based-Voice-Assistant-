# Voice Based AI Assistant

A fully local, Python-powered voice assistant that listens to your voice, understands it with OpenAI Whisper, thinks with Claude AI, and speaks back using offline TTS — no cloud audio processing required.

---

## Architecture

```
Microphone → [VAD Recorder] → [Whisper STT] → [Claude Brain] → [pyttsx3 TTS] → Speaker
```

| Layer | Technology | Notes |
|---|---|---|
| Speech-to-Text | faster-whisper | Runs locally, no API cost |
| AI Brain | Anthropic Claude (claude-sonnet-4-6) | With prompt caching |
| Text-to-Speech | pyttsx3 (SAPI5 on Windows) | Fully offline |
| Audio I/O | sounddevice + numpy | Cross-platform mic access |

---

## Project Structure

```
Hackculture/
├── voice_assistant/
│   ├── __init__.py
│   ├── config.py        # All settings (model sizes, thresholds, TTS rate)
│   ├── recorder.py      # Microphone input with energy-based VAD
│   ├── transcriber.py   # Whisper speech-to-text
│   ├── assistant.py     # Claude conversational brain
│   ├── speaker.py       # Text-to-speech output
│   └── pipeline.py      # Main conversation loop
├── main.py              # Entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## Prerequisites

- Python 3.10+
- A working microphone
- [Anthropic API key](https://console.anthropic.com/)

---

## Setup

**1. Clone and enter the project**

```bash
git clone <repo-url>
cd Hackculture
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

> On Windows, `sounddevice` may need the [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) if it doesn't install cleanly.

**3. Configure your environment**

```bash
copy .env.example .env   # Windows
# or
cp .env.example .env     # macOS / Linux
```

Edit `.env`:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
WHISPER_MODEL=base
WHISPER_DEVICE=cpu
WHISPER_COMPUTE=int8
```

**4. Run**

```bash
python main.py
```

---

## Usage

| Action | How |
|---|---|
| Start listening | Press **Enter** |
| Stop speaking | Just pause — VAD detects silence automatically |
| End session | Say **"exit"**, **"quit"**, or **"goodbye"** |
| Reset conversation | Say **"clear history"** |
| Force quit | Press **Ctrl+C** |

---

## Configuration

All settings live in [voice_assistant/config.py](voice_assistant/config.py) and can be overridden via `.env`.

| Setting | Default | Description |
|---|---|---|
| `WHISPER_MODEL` | `base` | `tiny` / `base` / `small` / `medium` / `large-v3` |
| `WHISPER_DEVICE` | `cpu` | Use `cuda` for NVIDIA GPU |
| `WHISPER_COMPUTE` | `int8` | Use `float16` on GPU |
| `SILENCE_THRESHOLD` | `0.015` | RMS amplitude to detect speech; raise if noisy env |
| `SILENCE_DURATION` | `1.5` | Seconds of silence before stopping recording |
| `TTS_RATE` | `175` | Words per minute for the TTS voice |
| `TTS_VOICE_INDEX` | `0` | Index into installed system voices |

**List available TTS voices:**

```bash
python -c "from voice_assistant.speaker import list_voices; print(list_voices())"
```

**Whisper model size trade-offs:**

| Model | Size | Speed | Accuracy |
|---|---|---|---|
| tiny | ~39 MB | Fastest | Basic |
| base | ~74 MB | Fast | Good |
| small | ~244 MB | Moderate | Better |
| medium | ~769 MB | Slow | High |
| large-v3 | ~1.5 GB | Slowest | Best |

---

## GPU Acceleration (Optional)

If you have an NVIDIA GPU with CUDA:

```bash
pip install faster-whisper[cuda]
```

Update `.env`:

```env
WHISPER_DEVICE=cuda
WHISPER_COMPUTE=float16
```

---

## Extending the Assistant

The modular design makes it easy to swap components:

- **Different STT**: Replace `transcriber.py` with Google STT, Azure, or Deepgram
- **Different TTS**: Swap `speaker.py` for ElevenLabs or Azure Neural TTS for better voice quality
- **Wake word**: Add a `wake_word.py` using `pvporcupine` to trigger recording hands-free
- **Tools / function calling**: Extend `assistant.py` with Claude tool use for web search, calendar, etc.

---

## Troubleshooting

**No audio captured**
- Check your default microphone in OS sound settings
- Lower `SILENCE_THRESHOLD` in `config.py` (try `0.008`)

**Whisper transcribes nothing / gibberish**
- Speak closer to the mic
- Try a larger model (`WHISPER_MODEL=small`)
- Ensure audio isn't clipping (reduce mic gain)

**pyttsx3 no sound**
- On Windows, ensure SAPI5 voices are installed (Control Panel → Speech)
- Try changing `TTS_VOICE_INDEX` to `1`

**`ANTHROPIC_API_KEY` error**
- Make sure `.env` exists (not just `.env.example`) and contains your key

---

## License

MIT
