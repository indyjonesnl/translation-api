# Use a lightweight Python base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn ollama pydantic

# Copy the script
COPY main.py .

# Expose the FastAPI port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]