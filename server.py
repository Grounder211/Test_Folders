from flask import Flask, request, send_from_directory, abort
import os

app = Flask(__name__)
DATA_DIR = '/data'  # K8s volume mount path

@app.route('/upload', methods=['POST'])
def upload_log():
    log_str = request.form.get('log')
    if not log_str:
        return "No log provided", 400

    filename = f"{log_str}.zip"
    file_path = os.path.join(DATA_DIR, filename)

    if os.path.isfile(file_path):
        return filename  # Send filename for client to download
    else:
        return "", 200  # No matching zip file

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    if os.path.isfile(os.path.join(DATA_DIR, filename)):
        return send_from_directory(DATA_DIR, filename, as_attachment=True)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
