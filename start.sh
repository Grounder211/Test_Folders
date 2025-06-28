#!/bin/bash

# Start Gunicorn to serve Flask app
gunicorn --bind 0.0.0.0:5000 server:app &

# Start nginx in foreground
nginx -g "daemon off;"
