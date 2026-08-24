from __future__ import annotations
from datetime import datetime
from .database import connect
from .schemas import MemoryItem

def now(): return datetime.now().astimezone().isoformat(timespec='seconds')

class ItemRepository:
    def upsert(self,item: MemoryItem):
        with connect() as db:
            row=db.execute('SELECT id FROM items WHERE kind=? AND description=? AND status="active"',(item.kind,item.description)).fetchone()
            if row:
                db.execute('UPDATE items SET content=?,keywords=?,due_at=?,priority=?,updated_at=? WHERE id=?',(item.content,item.keywords,item.due_at,item.priority,now(),row['id'])); return row['id']
            cur=db.execute('INSERT INTO items(kind,description,content,keywords,due_at,priority,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)',(item.kind,item.description,item.content,item.keywords,item.due_at,item.priority,now(),now())); return cur.lastrowid

    def active(self,limit=100):
        with connect() as db: return [dict(r) for r in db.execute('SELECT * FROM items WHERE status="active" ORDER BY priority DESC,updated_at DESC LIMIT ?',(limit,))]

    def update_status(self,item_id,status):
        with connect() as db: db.execute('UPDATE items SET status=?,updated_at=? WHERE id=?',(status,now(),item_id))

class HistoryRepository:
    def add(self,topic,summary,keywords='',source='conversation'):
        event_time=now()
        with connect() as db: db.execute('INSERT OR REPLACE INTO history(event_time,topic,summary,keywords,source) VALUES(?,?,?,?,?)',(event_time,topic,summary,keywords,source))
        return event_time

    def recent(self,limit=20):
        with connect() as db: return [dict(r) for r in db.execute('SELECT * FROM history ORDER BY event_time DESC LIMIT ?',(limit,))]
