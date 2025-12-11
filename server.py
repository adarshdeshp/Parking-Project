from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)

# Folder to save uploads
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload():
    img = request.data
    # Save with unique timestamp name
    filename = os.path.join(UPLOAD_FOLDER, f"vehicle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    with open(filename, "wb") as f:
        f.write(img)
    print(f"Received {len(img)} bytes → saved as {filename}")
    return "OK", 200

# Run server on all network interfaces
app.run(host="0.0.0.0", port=5000)
