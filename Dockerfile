# Use the Python 3.9 Slim Image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

# Install any dependencies
RUN apt-get update && pip install --upgrade pip && pip install -r requirements.txt

# Create a new user called 'app' with sudo privileges
RUN useradd -m app && echo "app ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch to the 'app' user
USER app

# Set the environment variable from .env file (OPENAI_API_KEY)
CMD ["streamlit", "run", "app.py"]