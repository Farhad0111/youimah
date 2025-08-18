# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the desired port
EXPOSE 8033

# Start the FastAPI server on port 8033
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8033"]
