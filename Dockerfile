# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Specify the command to run your Python script
CMD ["bash", "mkdir -p /app/images"]
CMD ["python", "price.py"]
CMD ["python", "send-price.py"]