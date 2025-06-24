FROM python:3.11-slim

WORKDIR /app

COPY server.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create data dir (mounted by K8s PVC)
RUN mkdir /data

EXPOSE 8080

CMD ["python", "server.py"]
