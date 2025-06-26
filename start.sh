#!/bin/bash

# Start Gunicorn in background
gunicorn --chdir server --bind 127.0.0.1:5000 wsgi:app &

# Start NGINX in foreground
nginx -g "daemon off;"
