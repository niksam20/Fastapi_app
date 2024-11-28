# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN python -m venv venv && \
    /bin/bash -c "source venv/bin/activate" && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the application will run on
EXPOSE 8000

# Command to start the application
CMD ["/bin/bash", "-c", "source venv/bin/activate && uvicorn app.api.main:app --host 0.0.0.0 --port 8000"]
