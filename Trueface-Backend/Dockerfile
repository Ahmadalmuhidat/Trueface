FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for MySQL client and building packages
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app source code
COPY . .

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Copy entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Use entrypoint to run migrations and start server
ENTRYPOINT ["/app/entrypoint.sh"]
