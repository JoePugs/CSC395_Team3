# Use the official Python image from the Docker Hub
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY app.py app.py

# Expose the port that Flask will run on
EXPOSE 5000

# Define the command to run the Flask app
CMD ["python", "app.py"]
