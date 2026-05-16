"""
Main conversation loop: record → transcribe → respond → speak.
"""

from __future__ import annotations

from voice_assistant.recorder import record_until_silence
from voice_assistant.transcriber import transcribe
from voice_assistant.assistant import VoiceAssistant
from voice_assistant.speaker import speak

EXIT_PHRASES = {"exit", "quit", "goodbye", "bye", "stop", "that's all"}


def run() -> None:
    print("\n=== Voice AI Assistant ===")
    print("Commands: say 'exit' / 'quit' / 'goodbye' to stop.")
    print("          say 'clear history' to reset the conversation.\n")

    assistant = VoiceAssistant()
    speak("Hello! I'm your voice assistant. How can I help you?")

    while True:
        try:
            input("Press Enter to speak (Ctrl+C to quit)...\n")
        except KeyboardInterrupt:
            _goodbye(assistant)
            return

        # --- Record ---
        audio = record_until_silence()
        if audio is None or len(audio) == 0:
            print("  [No audio captured — try again]\n")
            continue

        # --- Transcribe ---
        print("  [Transcribing...]")
        text = transcribe(audio)
        if not text:
            print("  [Could not understand — please try again]\n")
            continue

        print(f"\nYou: {text}")

        # --- Control phrases ---
        lower = text.lower().strip().rstrip(".")
        if lower in EXIT_PHRASES:
            _goodbye(assistant)
            return

        if "clear history" in lower or "reset conversation" in lower:
            assistant.clear()
            reply = "Conversation history cleared. Starting fresh!"
            print(f"Assistant: {reply}\n")
            speak(reply)
            continue

        # --- Claude ---
        print("  [Thinking...]")
        try:
            reply = assistant.respond(text)
        except Exception as exc:
            reply = "Sorry, I ran into an error. Please try again."
            print(f"  [Error: {exc}]")

        print(f"Assistant: {reply}\n")
        speak(reply)


def _goodbye(assistant: VoiceAssistant) -> None:
    msg = f"Goodbye! We had {assistant.turn_count} exchanges."
    print(f"\n{msg}")
    speak("Goodbye!")
