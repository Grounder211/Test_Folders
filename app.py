from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)

DATA_DIR = "/data/files"

@app.route('/')
def index():
    return "File Server is Running"

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    save_path = os.path.join(DATA_DIR, f.filename)
    f.save(save_path)
    return jsonify({"message": "File uploaded successfully."})

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(DATA_DIR, filename, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
