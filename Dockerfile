# Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirments.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirments.txt

# Copy the entire project
COPY . /app/

# Apply migrations
RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]