FROM python:3.9-slim

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -d /home/appuser -m appuser

WORKDIR /app

# Copy dependencies file first for better caching
COPY pyreq.txt .

# Install dependencies
RUN pip install --no-cache-dir -r pyreq.txt

# Copy application code
COPY . .

# Set proper permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 7000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7000/health || exit 1

# Command to run the application
CMD ["python", "app.py"]
