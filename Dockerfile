# Use official Python 3.13 slim image
FROM python:3.13-slim
 
# Set working directory
WORKDIR /app
 
# Copy requirements first (for Docker layer caching)
COPY req.txt .
 
# Install dependencies
RUN pip install --no-cache-dir -r req.txt
 
# Copy the rest of the application
COPY . .
 
# Create instance directory for SQLite database
RUN mkdir -p instance
 
# Expose port 5000
EXPOSE 5000
 
# Run with gunicorn (already in req.txt)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
