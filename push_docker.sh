#!/bin/bash

# Define your Docker image name
IMAGE_NAME="julianfl0w/bodypix"
# Define the tag for your image, for example, "latest" or "v1.0"
IMAGE_TAG="latest"

# Navigate to your Dockerfile directory if it's not in the current directory
# cd /path/to/your/dockerfile

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

# Push the Docker image to Docker Hub
echo "Pushing ${IMAGE_NAME}:${IMAGE_TAG} to Docker Hub..."
docker push ${IMAGE_NAME}:${IMAGE_TAG}

# Check if the push was successful
if [ $? -eq 0 ]; then
    echo "Docker image pushed successfully."
else
    echo "Failed to push Docker image to Docker Hub."
    exit 1
fi

echo "Done."
