import os
from flask import Flask, send_from_directory, abort, request

app = Flask(__name__)

ZIP_DIR = os.environ.get("ZIP_DIR", "/data")

@app.route("/download")
def download_file():
    filename = request.args.get("file")
    if not filename:
        return "Please specify a file parameter, e.g. /download?file=example.zip", 400

    # Secure against directory traversal (optional but recommended)
    if ".." in filename or filename.startswith("/"):
        return "Invalid filename", 400

    file_path = os.path.join(ZIP_DIR, filename)
    if not os.path.isfile(file_path):
        abort(404, description="File not found")

    return send_from_directory(ZIP_DIR, filename, as_attachment=True)

@app.route("/")
def index():
    return "Welcome to Zip Server! Use /download?file=filename.zip to download."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
