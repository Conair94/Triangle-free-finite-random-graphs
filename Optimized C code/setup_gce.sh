#!/bin/bash

# Exit on error
set -e

echo "Starting setup..."

# 1. Update system packages
echo "Updating system..."
sudo apt-get update
sudo apt-get install -y git python3-pip build-essential wget

# 2. Install Nauty (tools and headers)
# Ubuntu has a 'nauty' package for binaries (geng) and 'libnauty-dev' for headers
echo "Installing Nauty..."
sudo apt-get install -y nauty libnauty-dev

# 3. Install Python dependencies
echo "Installing Python requirements..."
# Assuming requirements.txt is in the same directory
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    pip3 install google-cloud-bigquery
fi

# 4. Verify installation
echo "Verifying installation..."
if ! command -v geng &> /dev/null; then
    echo "Error: 'geng' command not found. Nauty installation failed."
    exit 1
fi

echo "Setup complete! You can now run the gcp_runner.py script."
echo "Example usage:"
echo "python3 gcp_runner.py --project YOUR_PROJECT_ID --dataset YOUR_DATASET --table YOUR_TABLE --start-n 15 --end-n 16"
