# Moh-Reels 🎥

A lightweight **TikTok-like short video sharing app** built with Python Flask for backend and vanilla JavaScript for frontend.  
Users can upload short videos, view them in an infinite vertical scroll reels format, and enjoy seamless playback — all running locally or hosted online.

---

## 🚀 Features

- Upload short videos (`.mp4`, `.webm`, `.ogg`, `.mov`, `.mkv`) through a simple web interface.
- Videos are saved on the server and displayed instantly to all users.
- Vertical reels UI with autoplay/pause on scroll (like TikTok).
- Responsive and mobile-friendly.
- Minimal dependencies and easy to run locally or deploy online.
- Basic file type and upload size validation.
- Ready for extension with user accounts, likes, comments, and cloud storage.

---

## 🛠️ Tech Stack

- **Backend:** Python 3 + Flask  
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)  
- **Storage:** Local folder (`videos/`) for uploaded videos  
- **Deployment:** Compatible with free hosting providers (Render, Railway, etc.)

---

## 📥 Getting Started (Local Setup)

### Prerequisites

- Python 3.7+ installed
- Git (optional, for cloning)

### Steps

```bash
git clone https://github.com/mohamedboukerche22/Reels.git
cd Reels

# virtual environment (Linux/Mac)
python3 -m venv venv
source venv/bin/activate

# (Windows)
# python -m venv venv
# venv\Scripts\activate

pip install -r requirements.txt

# Run the app
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

# 📂 Project Structure
```

moh-reels/
├── app.py               # Flask backend app
├── requirements.txt     # Python dependencies
├── videos/              # Uploaded videos
├── templates/
│   └── index.html       # Frontend 
└── static/
    ├── styles.css       # CSS styles
    └── script.js        # Frontend JavaScript
```
# 🙏 Thanks

Inspired by TikTok and the amazing open-source community.
Built by Mohamed Boukerche.

