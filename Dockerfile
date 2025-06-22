# Use Ubuntu-based Python image
FROM python:3.10

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including Tesseract
RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    python3-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port (Render uses it automatically)
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
