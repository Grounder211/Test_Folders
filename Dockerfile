FROM python:3.11-slim

WORKDIR /app

COPY server.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update \
    && apt-get install -y nginx \
    && rm -rf /var/lib/apt/lists/*

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]
