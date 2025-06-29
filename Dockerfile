FROM python:3.10-alpine

# Install Flask
RUN pip install flask

# Create working directory
WORKDIR /app

# Copy app.py
COPY app.py .

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
