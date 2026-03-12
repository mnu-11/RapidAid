import sqlite3

DB_FILE = "users.db"

def create_post(title, content, author):
    """Add a new post to the database."""
    if not all([title, content, author]):
        return {"status": "error", "message": "All fields required"}

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
    c.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)", (title, content, author))
    conn.commit()
    conn.close()

    return {"status": "success", "message": "Post created successfully"}
