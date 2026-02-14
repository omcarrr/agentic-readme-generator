# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /workspace

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app/ ./app/

# Expose the FastAPI port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "8000"]