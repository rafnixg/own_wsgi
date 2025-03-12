#!/bin/bash

# Check if a container with the same name already exists and remove it
if [ "$(docker ps -aq -f name=own_wsgi)" ]; then
    docker rm -f own_wsgi
fi

# Run the Docker container
docker run -p 8081:8081 -rm -d --name own_wsgi own_wsgi_image