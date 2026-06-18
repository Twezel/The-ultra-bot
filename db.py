import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tracks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    url TEXT,
    last TEXT
)
""")

conn.commit()


def add_track(uid, url):
    cur.execute(
        "INSERT INTO tracks(user_id,url,last) VALUES(?,?,?)",
        (uid, url, "")
    )
    conn.commit()


def get_tracks():
    cur.execute("SELECT * FROM tracks")
    return cur.fetchall()


def update_track(tid, val):
    cur.execute("UPDATE tracks SET last=? WHERE id=?", (val, tid))
    conn.commit()
