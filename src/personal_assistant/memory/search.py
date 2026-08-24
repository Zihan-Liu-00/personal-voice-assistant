from __future__ import annotations
import re
from .database import connect

def terms(text): return [x.lower() for x in re.findall(r'[\u4e00-\u9fff]{2,}|[A-Za-z0-9_]{2,}',text)]

def search(query,limit=8):
    qs=terms(query)
    if not qs: return []
    with connect() as db:
        items=[dict(r) for r in db.execute('SELECT * FROM items WHERE status="active"')]
        history=[dict(r) for r in db.execute('SELECT * FROM history ORDER BY event_time DESC LIMIT 200')]
    scored=[]
    for row in items:
        hay=' '.join(str(row.get(k,'')) for k in ('kind','description','content','keywords','due_at')).lower(); score=sum(q in hay for q in qs)
        if score: scored.append((score,row))
    for row in history:
        hay=' '.join(str(row.get(k,'')) for k in ('topic','summary','keywords')).lower(); score=sum(q in hay for q in qs)
        if score: scored.append((score,row|{'kind':'history'}))
    scored.sort(key=lambda x:(-x[0],str(x[1].get('updated_at',x[1].get('event_time','')))),reverse=False)
    return [row for _,row in scored[:limit]]
