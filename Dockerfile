# Use the Python 3.8 image as the base
FROM python:3.8

# Install system dependencies (libgl1-mesa-glx for cv2)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx

# Set the working directory within the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Specify the command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
