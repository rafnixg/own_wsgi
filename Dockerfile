# Use an official Python runtime as a parent image
FROM python:3.11.2-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir .

# Make port 8081 available to the world outside this container
EXPOSE 8081

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["python3", "./main.py"]