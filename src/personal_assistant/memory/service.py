from __future__ import annotations
import re
from .database import init_db
from .repositories import ItemRepository,HistoryRepository
from .schemas import MemoryItem
from .search import search

class MemoryService:
    def __init__(self): init_db(); self.items=ItemRepository(); self.history=HistoryRepository()
    def search(self,query,limit=8): return search(query,limit)
    def upsert(self,kind,description,content,keywords='',due_at=None,priority=0): return self.items.upsert(MemoryItem(kind,description,content,keywords,due_at,priority))
    def context(self,query,limit=8):
        rows=self.search(query,limit)
        return '\n'.join(f"[{r.get('kind')}] {r.get('description')}: {r.get('content') or r.get('summary')}" for r in rows)
    def capture_explicit(self,text):
        # Deliberate, low-cost writes only. Routine transient questions are ignored.
        if not re.search(r'记住|以后|默认|偏好|提醒我|待办',text): return None
        if re.search(r'提醒我|待办',text): kind='todo'
        elif re.search(r'偏好|默认',text): kind='preference'
        else: kind='long_term'
        description=text[:40]; keywords=','.join(re.findall(r'[\u4e00-\u9fff]{2,}|[A-Za-z0-9_]{2,}',text)[:8])
        return self.upsert(kind,description,text,keywords)
