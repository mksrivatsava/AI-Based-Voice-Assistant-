"""
Claude-powered conversational brain.

Uses prompt caching on the system prompt (cache_control: ephemeral)
so repeated turns don't re-bill that token block.
"""

from __future__ import annotations

import anthropic

import voice_assistant.config as cfg


class VoiceAssistant:
    def __init__(self) -> None:
        if not cfg.ANTHROPIC_API_KEY:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY is not set. Add it to your .env file."
            )
        self.client = anthropic.Anthropic(api_key=cfg.ANTHROPIC_API_KEY)
        self.history: list[dict] = []

    # ------------------------------------------------------------------
    def respond(self, user_text: str) -> str:
        self.history.append({"role": "user", "content": user_text})

        response = self.client.messages.create(
            model=cfg.CLAUDE_MODEL,
            max_tokens=cfg.CLAUDE_MAX_TOKENS,
            system=[
                {
                    "type": "text",
                    "text": cfg.SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},  # prompt caching
                }
            ],
            messages=self.history,
        )

        reply = response.content[0].text
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def clear(self) -> None:
        self.history.clear()

    @property
    def turn_count(self) -> int:
        return len(self.history) // 2
