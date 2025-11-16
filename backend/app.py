from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # allow frontend access

# Folder to save images
VIOLATION_DIR = os.path.join(os.path.dirname(__file__), "../violations")
os.makedirs(VIOLATION_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_image():
    # ESP32 will send the image as a file
    file = request.files.get("image")
    if file:
        filename = f"violation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(VIOLATION_DIR, filename)
        file.save(filepath)
        return jsonify({"message": "Image received", "filename": filename}), 200
    return jsonify({"error": "No image received"}), 400

@app.route("/violations")
def list_images():
    files = os.listdir(VIOLATION_DIR)
    images = [f"http://localhost:5000/violations/{f}" for f in files if f.endswith(('.jpg', '.png'))]
    return jsonify(images)

@app.route("/violations/<path:filename>")
def serve_image(filename):
    return send_from_directory(VIOLATION_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
