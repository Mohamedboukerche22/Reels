import os
import shutil
from flask import (
    Flask, request, jsonify, render_template, send_from_directory,
    redirect, url_for, flash, session
)
from werkzeug.utils import secure_filename
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key =  os.urandom(24)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")  
UPLOAD_FOLDER = "videos"
ALLOWED_EXTENSIONS = {"mp4", "webm", "ogg", "mov", "mkv"}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# Create videos folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Visits counter file
VISITS_FILE = "visits.txt"

# -----------------------
# Helper functions
# -----------------------

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def increment_visits():
    if not os.path.exists(VISITS_FILE):
        with open(VISITS_FILE, "w") as f:
            f.write("0")
    with open(VISITS_FILE, "r+") as f:
        count = int(f.read())
        count += 1
        f.seek(0)
        f.write(str(count))
        f.truncate()

def get_visits_count():
    if not os.path.exists(VISITS_FILE):
        return 0
    with open(VISITS_FILE, "r") as f:
        return int(f.read())

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

# -----------------------
# Routes
# -----------------------

@app.route("/")
def index():
    increment_visits()
    videos = os.listdir(app.config["UPLOAD_FOLDER"])
    videos = sorted(videos, reverse=True)  # newest first
    return render_template("index.html", videos=videos)

@app.route("/upload", methods=["POST"])
def upload():
    if "video" not in request.files:
        return jsonify({"error": "No video file part"}), 400
    file = request.files["video"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Prevent overwriting by prefixing timestamp
        timestamp = int(os.path.getmtime(app.config["UPLOAD_FOLDER"]) if os.path.exists(app.config["UPLOAD_FOLDER"]) else 0)
        filename = f"{timestamp}_{filename}"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)
        return jsonify({"message": "Upload successful"}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route("/videos/<path:filename>")
def serve_video(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# -------- Admin routes --------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        pw = request.form.get("password", "")
        if pw == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid password")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

@app.route("/admin")
@admin_required
def admin_dashboard():
    videos = os.listdir(app.config["UPLOAD_FOLDER"])
    video_files = []
    for v in videos:
        path = os.path.join(app.config["UPLOAD_FOLDER"], v)
        size = os.path.getsize(path)
        video_files.append({"name": v, "size": size})
    total, used, free = shutil.disk_usage(app.config["UPLOAD_FOLDER"])
    visits = get_visits_count()
    return render_template(
        "admin_dashboard.html",
        videos=video_files,
        total=total,
        used=used,
        free=free,
        visits=visits,
    )

@app.route("/admin/delete/<filename>", methods=["POST"])
@admin_required
def delete_video(filename):
    safe_filename = secure_filename(filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], safe_filename)
    if os.path.exists(path):
        os.remove(path)
        flash(f"Deleted {safe_filename}")
    else:
        flash("File not found")
    return redirect(url_for("admin_dashboard"))

# -----------------------
# Run server
# -----------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
