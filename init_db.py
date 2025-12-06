import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "forum.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

with sqlite3.connect(DB_PATH) as conn, open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    conn.executescript(f.read())

print("Database initialized at", DB_PATH)
