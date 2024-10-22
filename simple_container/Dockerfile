# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app/

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    usbutils \
    vim \
    && rm -rf /var/lib/apt/lists/*

CMD ["tail", "-f", "/app/test_file.log"]
