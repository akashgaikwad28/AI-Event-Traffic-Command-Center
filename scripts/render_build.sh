#!/usr/bin/env bash
# Exit on error
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Configuring writable directories for Render..."
export TMPDIR="$PWD/tmp"
mkdir -p "$TMPDIR"
export DVC_TEMPDIR="$TMPDIR"
export XDG_CACHE_HOME="$TMPDIR"
export XDG_CONFIG_HOME="$TMPDIR"
export XDG_DATA_HOME="$TMPDIR"
export DVC_NO_ANALYTICS=true
export DVC_SYSTEM_CONFIG_DIR="$TMPDIR"
export DVC_GLOBAL_CONFIG_DIR="$TMPDIR"
export DVC_SITE_CACHE_DIR="$TMPDIR"


echo "Configuring DVC authentication for DagsHub..."
# We use the $DAGSHUB_USER_TOKEN securely injected by Render
dvc remote modify origin --local auth basic
dvc remote modify origin --local user akash.gaikwad9945
dvc remote modify origin --local password $DAGSHUB_USER_TOKEN

echo "Pulling machine learning models and datasets from DVC..."
dvc pull -r origin

echo "Build complete! Models are ready for inference."
