#!/bin/bash

# Build script for unified deployment
echo "Starting unified build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
cd backend
pip install -r requirements.txt

# Return to root and build frontend
echo "Building frontend..."
cd ../frontend

# Check if npm is available, if not try alternative approaches
if command -v npm &> /dev/null; then
    npm install
    npm run build
elif command -v yarn &> /dev/null; then
    yarn install
    yarn build
else
    echo "Error: Neither npm nor yarn found. Please ensure Node.js is available."
    exit 1
fi

echo "Build completed successfully!"
