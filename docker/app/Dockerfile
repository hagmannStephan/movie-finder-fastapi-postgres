# Use an official Python image as the base
FROM python:3.12-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && [ -f requirements.txt ] && pip install -r requirements.txt || echo "No requirements.txt found"

# Copy the rest of the application files
COPY . /app/

# Expose the application port
EXPOSE 8000

# Run FastAPI automatically on container start with reload enabled
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
