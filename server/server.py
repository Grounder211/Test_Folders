from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)
ZIP_DIR = os.path.join(os.path.dirname(__file__), 'data')

@app.route('/download', methods=['GET'])
def download_zip():
    filename = request.args.get('file')
    if not filename:
        return jsonify({"error": "Missing file parameter"}), 400
    filepath = os.path.join(ZIP_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_from_directory(ZIP_DIR, filename, as_attachment=True)
