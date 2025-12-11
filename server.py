from flask import Flask, request, send_from_directory, send_file, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import glob

app = Flask(__name__)
CORS(app)  # allow all devices to access API

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------------------------------------------------
# 🔹 Upload Image from ESP32
# ---------------------------------------------------
@app.route("/upload", methods=["POST"])
def upload():
    try:
        img = request.data
        if not img:
            return "NO IMAGE RECEIVED", 400

        filename = f"vehicle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(img)

        print(f"Saved: {filepath}")
        return "OK", 200

    except Exception as e:
        print("ERROR:", e)
        return "SERVER ERROR", 500


# ---------------------------------------------------
# 🔹 Latest Uploaded Image
# ---------------------------------------------------
@app.route("/latest-image")
def latest_image():
    files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.jpg"))
    if not files:
        return "No IMAGE", 404
    latest = max(files, key=os.path.getctime)
    return send_file(latest, mimetype="image/jpeg")


# ---------------------------------------------------
# 🔹 Return List of All Violations (IMAGE URLs)
# ---------------------------------------------------
@app.route("/violations")
def violations():
    files = sorted(os.listdir(UPLOAD_FOLDER))
    
    # Automatically detect server IP (10.x.x.x or 192.x.x.x)
    base = request.host_url.rstrip("/")
    
    urls = [f"{base}/uploads/{f}" for f in files if f.endswith(".jpg")]
    return jsonify(urls)


# ---------------------------------------------------
# 🔹 Serve Uploaded Files (Image Hosting)
# ---------------------------------------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ---------------------------------------------------
# 🔹 Root
# ---------------------------------------------------
@app.route("/")
def home():
    return "Smart Parking Server is running!"


# ---------------------------------------------------
# Run Flask App
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
