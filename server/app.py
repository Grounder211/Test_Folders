from flask import Flask, send_from_directory, abort
import os, datetime

app = Flask(__name__)
FILE_DIR = "/data/files"
LOG_FILE = "/data/logs/missing_requests.log"

os.makedirs(FILE_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

@app.route("/file/<filename>")
def serve_file(filename):
    path = os.path.join(FILE_DIR, filename)
    if os.path.exists(path):
        return send_from_directory(FILE_DIR, filename, as_attachment=True)
    else:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.datetime.now().isoformat()} - MISSING: {filename}\n")
        abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
