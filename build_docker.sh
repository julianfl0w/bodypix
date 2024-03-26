#!/bin/bash

# Define your Docker image name
IMAGE_NAME="julianfl0w/bodypix"
# Define the tag for your image, for example, "latest" or "v1.0"
IMAGE_TAG="latest"

# Build the Docker image
echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

# Check if the build was successful
if [ $? -eq 0 ]; then
    echo "Docker image built successfully."
else
    echo "Docker image build failed."
    exit 1
fi
