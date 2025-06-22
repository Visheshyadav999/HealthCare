# Use official Python image
FROM python:3.10-slim

# Install system packages including tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port (Render auto-detects)
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
