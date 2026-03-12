import sqlite3

DB_FILE = "users.db"

def search_post(query=""):
    """Search posts by title or content."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

    if query.strip():
        c.execute("""
            SELECT id, title, content, author FROM posts
            WHERE title LIKE ? OR content LIKE ?
        """, (f"%{query}%", f"%{query}%"))
    else:
        c.execute("SELECT id, title, content, author FROM posts")

    rows = c.fetchall()
    conn.close()

    posts = [{"id": r[0], "title": r[1], "content": r[2], "author": r[3]} for r in rows]
    return posts
