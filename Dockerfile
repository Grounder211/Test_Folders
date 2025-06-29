FROM alpine:latest

# Install minimal web server (BusyBox's httpd)
RUN apk add --no-cache busybox

# Create working dir
RUN mkdir -p /data

# Add shell script to start the server
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run busybox http server
CMD ["/start.sh"]
