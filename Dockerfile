# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code into the container
COPY ./app /code/app

# Expose the port the app runs on
EXPOSE 8000

# Run uvicorn server.
# The host 0.0.0.0 makes the server accessible from outside the container.
# The --port will be set by Render automatically, but we can default it.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]