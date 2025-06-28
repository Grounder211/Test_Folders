# Use an official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only the necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose port Flask runs on
EXPOSE 5000

# Environment variable (optional default)
ENV ZIP_DIR=/data

# Command to run your server directly
CMD ["python", "app.py"]
