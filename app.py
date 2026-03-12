from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Import your modules
from create_post import create_post
from search_post import search_post
from edit_post import edit_post
from feedback import add_feedback, get_feedback

app = Flask(__name__)
DB_FILE = "users.db"

# ----------------- Database Initialization -----------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # Posts table
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)
    # Feedback table
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            feedback TEXT NOT NULL,
            rating INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------- User Routes -----------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"status": "error", "message": "All fields required"})
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Signup successful"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Username already exists"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "error", "message": "Invalid username or password"})

# ----------------- Post Routes -----------------
@app.route("/create_post", methods=["POST"])
def create_post_route():
    data = request.json
    title = data.get("title")
    content = data.get("content")
    author = data.get("author")
    return jsonify(create_post(title, content, author))

@app.route("/search_post", methods=["GET"])
def search_post_route():
    q = request.args.get("q", "")
    return jsonify(search_post(q))

@app.route("/edit_post", methods=["POST"])
def edit_post_route():
    data = request.json
    post_id = data.get("id")
    new_title = data.get("title")
    new_content = data.get("content")
    return jsonify(edit_post(post_id, new_title, new_content))

# ----------------- Feedback Routes -----------------
@app.route("/add_feedback", methods=["POST"])
def add_feedback_route():
    data = request.json
    username = data.get("username")
    feedback_text = data.get("feedback")
    rating = data.get("rating")

    if not all([username, feedback_text, rating]):
        return jsonify({"status": "error", "message": "All fields required"})

    try:
        rating = int(rating)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid rating"})

    try:
        result = add_feedback(username, feedback_text, rating)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})

@app.route("/get_feedback")
def get_feedback_route():
    return jsonify(get_feedback())

# ----------------- Home Route -----------------
@app.route("/")
def home():
    return render_template("index.html")

# ----------------- SOS Alert Route -----------------
@app.route("/sos", methods=["POST"])
def sos_alert():
    data = request.json
    username = data.get("username", "Unknown User")

    sender = "rajrawat2557@gmail.com"     # replace with your Gmail
    receiver = "rajrawat200403@gmail.com"
    password = "vsjx wtkf kryy rxzz" # Gmail app password

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "🚨 SOS Alert from Emergency Health System"
    body = f"SOS alert triggered by user: {username}\n\nPlease respond immediately!"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        return jsonify({"status": "success", "message": "🚨 SOS email sent successfully!"})
    except Exception as e:
        print("Error sending SOS:", e)
        return jsonify({"status": "error", "message": f"Failed to send SOS: {str(e)}"})

# ----------------- Run App -----------------
if __name__ == "__main__":
    app.run(debug=True)
