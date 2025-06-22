#!/usr/bin/env bash

# Install Tesseract and required libraries
apt-get update && apt-get install -y tesseract-ocr

# Optional: Install language packs if needed (like Hindi, etc.)
# apt-get install -y tesseract-ocr-hin
