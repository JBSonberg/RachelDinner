FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local directory contents to the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run gunicorn with multiple workers on port 80 and bind to 0.0.0.0
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]


