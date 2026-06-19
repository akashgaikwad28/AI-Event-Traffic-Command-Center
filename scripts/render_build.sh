#!/usr/bin/env bash
# Exit on error
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Configuring DVC authentication for DagsHub..."
# We use the $DAGSHUB_USER_TOKEN securely injected by Render
dvc remote modify origin --local auth basic
dvc remote modify origin --local user akash.gaikwad9945
dvc remote modify origin --local password $DAGSHUB_USER_TOKEN

echo "Pulling machine learning models and datasets from DVC..."
dvc pull

echo "Build complete! Models are ready for inference."
