FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /server

# Copy server script into the container
COPY server.py .

# Install Flask
RUN pip install flask

# Environment variable to match host path
ENV ZIP_DIR="C:/Users/Public/Downloads/DATA_Files"

EXPOSE 5000

CMD ["python", "server.py"]
