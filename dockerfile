# Use NVIDIA CUDA with Ubuntu as the base image
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Set working directory inside the container
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Install Node.js, npm, and other dependencies
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    # Clean up APT when done to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    npm install @tensorflow/tfjs-node && \
    # If using GPU, you can uncomment the line below and comment out the tfjs-node installation line
    # npm install @tensorflow/tfjs-node-gpu && \
    npm install

# Expose the port your app runs on
EXPOSE 5000

# Start the server
CMD ["node", "bodypix.js"]
