# Use the official Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the server files to the working directory
COPY . .

# Set the environment variables if needed
# ENV VARIABLE_NAME=value

# Expose the port on which your server listens
EXPOSE 5000

# Start the server
CMD ["python", "app.py"]