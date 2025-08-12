from flask import *
import os
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = "videos"
ALLOWED_EXTENSIONS = {"mp4", "webm", "ogg", "mov", "mkv"}
MAX_CONTENT_LENGTH = 200 * 1024 * 1024  

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.secret_key = os.urandom(24)  

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "video" not in request.files:
        flash("No file part")
        return redirect(url_for("index"))
    file = request.files["video"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("index"))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # add timestamp to avoid collisions
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        filename = f"{ts}_{filename}"
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        return jsonify({"success": True, "filename": filename})
    else:
        return jsonify({"success": False, "error": "invalid file type"}), 400

@app.route("/api/videos")
def list_videos():
    files = []
    for name in sorted(os.listdir(app.config["UPLOAD_FOLDER"]), reverse=True):
        if allowed_file(name):
            full = os.path.join(app.config["UPLOAD_FOLDER"], name)
            stat = os.stat(full)
            files.append({
                "filename": name,
                "url": url_for("serve_video", filename=name),
                "size": stat.st_size,
                "mtime": int(stat.st_mtime)
            })
    return jsonify(files)

@app.route("/videos/<path:filename>")
def serve_video(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, conditional=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
