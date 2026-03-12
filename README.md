🚨 SafeSignal – Emergency Alert & Community Support System
📌 Overview

SafeSignal is a web-based application built using Python and Flask that allows users to share emergency-related posts, provide feedback, and send SOS alerts via email during critical situations.

The system helps users quickly notify emergency contacts and share important information with the community.

🎯 Features

👤 User Authentication – Signup and Login system

📝 Create Posts – Users can share emergency updates or information

🔎 Search Posts – Find posts using keywords

✏️ Edit Posts – Update existing posts

⭐ Feedback System – Users can submit feedback and ratings

🚨 SOS Alert System – Send emergency email alerts instantly

🛠 Technologies Used

Python

Flask

SQLite Database

HTML

CSS

SMTP (Email Service)

📂 Project Structure
emergency_blog/
│
├── app.py
├── create_post.py
├── edit_post.py
├── search_post.py
├── feedback.py
├── users.db
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/yourusername/projectname.git
2️⃣ Go to project directory
cd projectname
3️⃣ Install dependencies
pip install flask
4️⃣ Run the application
python app.py
5️⃣ Open in browser
http://127.0.0.1:5000
🚨 SOS Alert Feature

When the SOS button is triggered:

An emergency email alert is sent

The message notifies emergency contacts immediately

🔮 Future Improvements

Password hashing for better security

GPS location sharing during SOS

Mobile responsive UI

Emergency contact management

Admin dashboard
