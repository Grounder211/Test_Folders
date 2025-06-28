from flask import Flask, request, send_from_directory, abort
import os

app = Flask(__name__)

# Get ZIP directory from environment variable, default to /data
ZIP_DIR = os.environ.get("ZIP_DIR", "/data")

@app.route('/')
def index():
    files = os.listdir(ZIP_DIR)
    return {
        "available_files": [f for f in files if f.endswith('.zip')]
    }

@app.route('/download')
def download():
    filename = request.args.get('file')
    if not filename:
        return {"error": "File parameter is required"}, 400

    file_path = os.path.join(ZIP_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}, 404

    return send_from_directory(ZIP_DIR, filename, as_attachment=True)

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
