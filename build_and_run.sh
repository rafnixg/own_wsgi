#!/bin/bash

# Build the Docker image
docker build -t own_wsgi_image .

# Check if a container with the same name already exists and remove it
if [ "$(docker ps -aq -f name=own_wsgi)" ]; then
    docker rm -f own_wsgi
fi

# Run the Docker container
docker run -p 8081:8081 --name own_wsgi own_wsgi_image
