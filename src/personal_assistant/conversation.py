from __future__ import annotations

from .config import CONFIG


class ConversationManager:
    """Keeps short-term turns in memory and archives older turns as summaries."""

    def __init__(self, llm, history_repo):
        self.llm = llm
        self.history_repo = history_repo
        self.turns: list[dict[str, str]] = []

    @staticmethod
    def _chars(turns):
        return sum(len(m.get('content', '')) for m in turns)

    def prepare(self, user_text: str, memory_context: str = ''):
        candidate = self.turns + [{'role': 'user', 'content': user_text}]
        extra = memory_context or ''
        if self._chars(candidate) + len(extra) > CONFIG.context_safe_chars:
            self._compact()
        return list(self.turns)

    def append(self, user_text: str, answer: str):
        self.turns.append({'role': 'user', 'content': user_text})
        self.turns.append({'role': 'assistant', 'content': answer})

    def _compact(self):
        keep = CONFIG.context_keep_turns * 2
        if len(self.turns) <= keep:
            return
        old, self.turns = self.turns[:-keep], self.turns[-keep:]
        transcript = '\n'.join(f"{m['role']}: {m['content']}" for m in old)
        summary = self.llm.summarize(transcript)
        self.history_repo.add('conversation', summary, source='conversation_compact')
