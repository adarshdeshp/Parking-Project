from flask import Flask, request, send_from_directory, send_file, jsonify, render_template
from flask_cors import CORS
import os
from datetime import datetime
import glob

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ================= Existing upload route =================
@app.route("/upload", methods=["POST"])
def upload():
    try:
        if not request.data:
            return "NO IMAGE RECEIVED", 400

        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
        path = os.path.join(UPLOAD_FOLDER, filename)

        with open(path, "wb") as f:
            f.write(request.data)

        print("Saved:", path)
        return "OK", 200

    except Exception as e:
        print("ERROR:", e)
        return "SERVER ERROR", 500

# ================= Route for latest image =================
@app.route("/latest-image")
def latest_image():
    list_of_files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.jpg"))
    if not list_of_files:
        return "No IMAGE", 404
    latest_file = max(list_of_files, key=os.path.getctime)
    return send_file(latest_file, mimetype="image/jpeg")

# ================= Existing routes =================
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Serve individual uploaded images
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Provide JSON list of all uploaded images for the dashboard
@app.route("/violations")
def violations():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".jpg")]
    # Convert backslashes to forward slashes for proper URLs
    urls = [f"http://10.173.184.189:5000/uploads/{f.replace('\\','/')}" for f in files]
    return jsonify(urls)

# Home route
@app.route("/")
def home():
    return "Server is running"

# ====================== Run Server =======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
