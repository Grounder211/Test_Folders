from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)
ZIP_DIR = os.environ.get("ZIP_DIR", "/data")

@app.route("/")
def index():
    return "Zip Server is Running"

@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(ZIP_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(ZIP_DIR, filename, as_attachment=True)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
