FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from parent directory
# We'll copy the requirements.txt into admin directory first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy admin application
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Expose port
EXPOSE 8000

# Run the admin application
CMD ["python", "main.py"]