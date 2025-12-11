from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    img = request.data
    with open("capture.jpg","wb") as f:
        f.write(img)
    print(f"Received {len(img)} bytes")
    return "OK", 200

# Important: 0.0.0.0 allows external devices to reach the server
app.run(host="0.0.0.0", port=5000)
