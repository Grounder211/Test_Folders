#!/usr/bin/env python3
"""
Secure File Server for LAN deployment
Handles file requests from clients within the same network
"""

import os
import logging
import zipfile
from pathlib import Path
from flask import Flask, request, jsonify, send_file, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour", "20 per minute"]
)

# Configuration
FILES_DIR = os.getenv('FILES_DIR', '/app/files')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Ensure files directory exists
Path(FILES_DIR).mkdir(parents=True, exist_ok=True)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'files_dir': FILES_DIR
    })

@app.route('/download', methods=['POST'])
@limiter.limit("10 per minute")
def download_file():
    """Download file endpoint - client sends filename, server returns file"""
    try:
        data = request.get_json()
        if not data or 'filename' not in data:
            logger.warning(f"Invalid request from {request.remote_addr}")
            return jsonify({'error': 'filename required'}), 400
        
        filename = data['filename']
        
        # Security: validate filename
        if not filename.endswith('.zip'):
            return jsonify({'error': 'Only .zip files allowed'}), 400
        
        # Secure the filename to prevent directory traversal
        secure_name = secure_filename(filename)
        file_path = Path(FILES_DIR) / secure_name
        
        logger.info(f"File request: {secure_name} from {request.remote_addr}")
        
        # Check if file exists
        if not file_path.exists():
            logger.warning(f"File not found: {secure_name}")
            return jsonify({'error': 'File not found'}), 404
        
        # Verify it's actually a zip file
        if not zipfile.is_zipfile(file_path):
            logger.error(f"Invalid zip file: {secure_name}")
            return jsonify({'error': 'Invalid zip file'}), 400
        
        logger.info(f"Sending file: {secure_name} to {request.remote_addr}")
        return send_file(
            file_path,
            as_attachment=True,
            download_name=secure_name,
            mimetype='application/zip'
        )
        
    except Exception as e:
        logger.error(f"Error in download_file: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/files', methods=['GET'])
def list_files():
    """List available zip files (for debugging)"""
    try:
        files_dir = Path(FILES_DIR)
        zip_files = [f.name for f in files_dir.glob('*.zip')]
        return jsonify({
            'files': zip_files,
            'count': len(zip_files)
        })
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        return jsonify({'error': 'Error listing files'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded'}), 429

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info(f"Starting file server on port {PORT}")
    logger.info(f"Files directory: {FILES_DIR}")
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
