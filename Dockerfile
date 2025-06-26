FROM python:3.11-slim

WORKDIR /app

COPY server /app/server
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update \
    && apt-get install -y nginx \
    && rm -rf /var/lib/apt/lists/*

# Gunicorn + NGINX entry
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80
CMD ["/start.sh"]
