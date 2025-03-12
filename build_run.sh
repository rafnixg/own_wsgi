#!/bin/bash

# Build the Docker image
echo "Building the Docker image..."
docker build -t own_wsgi_image .

# exit if the build failed
if [ $? -ne 0 ]; then
    echo "Docker image build failed!"
    exit 1
fi

echo "Docker image built successfully!"

