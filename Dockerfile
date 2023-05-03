# Use the official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Make the main.py file executable
RUN chmod +x main.py

# Create a symlink to make the script available as "rocket" command
RUN ln -s /app/main.py /usr/local/bin/rocket

# Set the entrypoint to the rocket script
ENTRYPOINT ["rocket"]
