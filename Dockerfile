# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /movie_rec_engine

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variable to tell Flask the app entry point
ENV FLASK_APP=movie_rec_engine.py

# Expose the port Flask is running on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "movie_rec_engine.py"]