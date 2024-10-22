# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app/

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    usbutils \
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create directories before using them

# Copy the requirements file to the container
# COPY requirements.txt /app/

COPY . /app/

# Install the required Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire project (code) to the temp folder

# Copy files from temp to dist (if needed for obfuscation)
# RUN cp -a /app/temp /app/dist/

# # Uncomment and adjust if you want to obfuscate your code at this stage
# RUN pyarmor gen -r --exclude "manage.py" -O /app/dist /app/temp/

# # Uncomment if using pyarmor runtime
# RUN mv /app/dist/pyarmor_runtime_000000 /app/dist/temp/pyarmor_runtime_000000

# RUN rm -rf /app/temp
# RUN mv  /app/dist/temp/* /app/
# RUN rm -rf /app/dist
# RUN mkdir dist
# RUN cp -a . !(dist) dist/
# RUN rsync -av . dist --exclude=dist/
# RUN pyarmor gen --exclude "dist/*" -O dist -r .
# RUN mv /app/dist/pyarmor_runtime_000000 /app/dist//pyarmor_runtime_000000

# Expose the port the app runs on
EXPOSE 8000
# RUN touch /app/file.log

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["sh", "-c", "echo 'Container started' >> /app/file.log && tail -f /app/file.log"]
