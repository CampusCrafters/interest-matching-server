# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN prisma generate

# Copy the application code to the container
COPY . .

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Start the FastAPI application
CMD ["python", "-m", "app.main"]