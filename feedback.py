
import sqlite3

DB_FILE = "users.db"


def init_feedback_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            feedback TEXT NOT NULL,
            rating INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_feedback_db()

def add_feedback(user, feedback, rating):
    if not all([user, feedback, rating]):
        return {"status": "error", "message": "All fields required"}
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO feedback (user, feedback, rating) VALUES (?, ?, ?)", (user, feedback, rating))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Feedback submitted successfully"}

def get_feedback():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user, feedback, rating FROM feedback ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    feedback_list = [{"username": r[0], "feedback": r[1], "rating": r[2]} for r in rows]
    return feedback_list
