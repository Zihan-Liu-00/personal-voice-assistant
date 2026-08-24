from dataclasses import dataclass
from typing import Literal

MemoryKind=Literal['preference','long_term','todo']

@dataclass
class MemoryItem:
    kind: MemoryKind
    description: str
    content: str
    keywords: str=''
    due_at: str|None=None
    priority: int=0
