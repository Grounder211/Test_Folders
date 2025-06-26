FROM python:3.10-slim
WORKDIR /app
COPY server.py requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir /app/data
ENV ZIP_DIR=/app/data
EXPOSE 5000
CMD ["python", "server.py"]
