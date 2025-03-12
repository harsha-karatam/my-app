# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Set environment variables for AWS credentials
# Replace <your-access-key-id> and <your-secret-access-key> with your actual AWS credentials
ENV AWS_ACCESS_KEY_ID=AKIA4WJPWSWVIBPVY22V
ENV AWS_SECRET_ACCESS_KEY=3kmpOBFMlE8g6UsORVM84K51m+FRBH21DiAWmzT+

# Install required dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /app

# Create a directory for uploads (if you want to store files locally as well)
RUN mkdir -p /app/uploads

# Expose the port for the Flask app
EXPOSE 5003

# Run the Flask app
CMD ["python", "app/main.py"]

