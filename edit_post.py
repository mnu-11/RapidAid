import sqlite3

DB_FILE = "users.db"

def edit_post(post_id, new_title, new_content):
    """Edit a post by ID."""
    if not all([post_id, new_title, new_content]):
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
    c.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (new_title, new_content, post_id))
    conn.commit()
    updated = c.rowcount
    conn.close()

    if updated:
        return {"status": "success", "message": "Post updated successfully"}
    else:
        return {"status": "error", "message": "Post not found"}
