# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app/

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    usbutils \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# obfuscate the code
# RUN mkdir dist
COPY . /app/home/
RUN mkdir dist
RUN cp -a /app/home dist/
RUN pyarmor gen -O dist -r /app/home/
RUN mv dist/pyarmor_runtime_000000 dist/django_app/pyarmor_runtime_000000

# Copy the entire Django project to the container

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]