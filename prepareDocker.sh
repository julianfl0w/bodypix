#!/bin/bash

# Install Node.js and npm
echo "Installing Node.js and npm..."
apt-get update
apt-get install -y nodejs npm

# Verify Node.js and npm installation
node -v
npm -v

# Install TensorFlow.js for Node.js
# Use @tensorflow/tfjs-node for CPU usage or @tensorflow/tfjs-node-gpu for GPU usage
echo "Installing TensorFlow.js for Node.js..."
npm install @tensorflow/tfjs-node

# If you have an NVIDIA GPU and want to use it, install the GPU version instead
# Uncomment the line below and comment out the tfjs-node installation line above
# npm install @tensorflow/tfjs-node-gpu

# Install other project dependencies from package.json
# Make sure you are in the project directory where package.json is located
echo "Installing project dependencies from package.json..."
npm install

# Start the server
# Make sure you are in the directory containing server.js
echo "Starting the server..."
node server.js
