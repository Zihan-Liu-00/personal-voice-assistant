from __future__ import annotations
import sqlite3
from pathlib import Path
from .config import DB_PATH

def connect(path: Path=DB_PATH):
    path.parent.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(path); db.row_factory=sqlite3.Row
    db.execute('PRAGMA journal_mode=WAL'); db.execute('PRAGMA foreign_keys=ON')
    return db

def init_db():
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          kind TEXT NOT NULL CHECK(kind IN ('preference','long_term','todo')),
          description TEXT NOT NULL,
          content TEXT NOT NULL,
          keywords TEXT NOT NULL DEFAULT '',
          status TEXT NOT NULL DEFAULT 'active',
          priority INTEGER NOT NULL DEFAULT 0,
          due_at TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_items_kind_status ON items(kind,status);
        CREATE TABLE IF NOT EXISTS history (
          event_time TEXT PRIMARY KEY,
          topic TEXT NOT NULL,
          summary TEXT NOT NULL,
          keywords TEXT NOT NULL DEFAULT '',
          source TEXT NOT NULL DEFAULT 'conversation'
        );
        CREATE INDEX IF NOT EXISTS idx_history_topic ON history(topic);
        ''')
