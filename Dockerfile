# Use a slim Python base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional, adjust if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
